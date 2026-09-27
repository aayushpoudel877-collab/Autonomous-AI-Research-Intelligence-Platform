from html.parser import HTMLParser
from urllib.request import Request, urlopen

from nexus.ingestion.base import Ingestor
from nexus.security.url_policy import validate_url
from nexus.types import SourceDocument
from nexus.utils import clean_text, stable_id


class _HTMLTextParser(HTMLParser):
    BLOCKED = {"script", "style", "noscript", "svg"}

    def __init__(self):
        super().__init__()
        self.parts = []
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.BLOCKED:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag.lower() in self.BLOCKED and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if not self.depth and data.strip():
            self.parts.append(data.strip())


class URLIngestor(Ingestor):
    def __init__(self, timeout=10, max_bytes=2_000_000):
        self.timeout = timeout
        self.max_bytes = max_bytes

    def ingest(self, source: str) -> SourceDocument:
        url = validate_url(source)
        request = Request(url, headers={"User-Agent": "NEXUS/0.2 research-ingestor"})
        with urlopen(request, timeout=self.timeout) as response:
            content_type = response.headers.get_content_type()
            if content_type != "text/html":
                raise ValueError(f"Unsupported web content type: {content_type}")
            body = response.read(self.max_bytes + 1)
        if len(body) > self.max_bytes:
            raise ValueError("Web document exceeds configured size limit")
        parser = _HTMLTextParser()
        parser.feed(body.decode("utf-8", errors="replace"))
        text = clean_text("\\n".join(parser.parts))
        if not text:
            raise ValueError("Web page contained no extractable text")
        title = url
        return SourceDocument(stable_id(url, text), title, text, url, {"content_type": content_type})
