from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


@dataclass(frozen=True)
class SourceCandidate:
    url: str
    title: str = ""
    provider: str = "unknown"
    score: float = 0.0


@dataclass(frozen=True)
class AcquiredSource:
    canonical_url: str
    title: str
    text: str
    provider: str
    quality: float
    content_hash: str
    fetched_at: str
    freshness_days: float


class SourceSearchProvider(Protocol):
    name: str

    def search(self, query: str, limit: int = 5) -> list[SourceCandidate]:
        ...


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    if parts.scheme.lower() not in {"http", "https"} or not parts.netloc:
        raise ValueError("Only absolute HTTP(S) URLs can be canonicalized")
    host = parts.hostname.lower() if parts.hostname else ""
    port = parts.port
    netloc = host
    if port and not ((parts.scheme.lower() == "http" and port == 80) or (parts.scheme.lower() == "https" and port == 443)):
        netloc = f"{host}:{port}"
    query = urlencode(sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() not in {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid", "gclid"}))
    return urlunsplit((parts.scheme.lower(), netloc, parts.path or "/", query, ""))


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
