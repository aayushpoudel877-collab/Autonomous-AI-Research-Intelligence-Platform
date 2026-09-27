from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib.request import HTTPRedirectHandler, Request, build_opener

from nexus.ingestion.base import Ingestor
from nexus.security.url_policy import validate_url
from nexus.types import SourceDocument
from nexus.utils import clean_text, stable_id


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


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
    def __init__(self, timeout=10, max_bytes=2_000_000, max_redirects=3):
        self.timeout = timeout
        self.max_bytes = max_bytes
        self.max_redirects = max_redirects
        self.opener = build_opener(_NoRedirect)

    def _fetch(self, url: str):
        current = validate_url(url)
        for _ in range(self.max_redirects + 1):
            request = Request(current, headers={"User-Agent": "NEXUS/0.2 research-ingestor"})
            try:
                response = self.opener.open(request, timeout=self.timeout)
            except Exception as exc:
                if getattr(exc, "code", None) in {301, 302, 303, 307, 308}:
                    location = exc.headers.get("Location")
                    if not location:
                        raise ValueError("Redirect response did not provide a destination") from exc
                    current = validate_url(urljoin(current, location))
                    continue
                raise ValueError(f"Unable to fetch URL: {exc}") from exc
            return current, response
        raise ValueError("Too many redirects")

    def ingest(self, source: str) -> SourceDocument:
        url = validate_url(source)
        final_url, response = self._fetch(url)
        with response:
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
        return SourceDocument(
            stable_id(final_url, text),
            final_url,
            text,
            final_url,
            {"content_type": content_type},
        )
