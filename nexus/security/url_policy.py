from ipaddress import ip_address
from urllib.parse import urlparse
import socket

ALLOWED_SCHEMES = {"http", "https"}


def validate_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES or not parsed.hostname:
        raise ValueError("Only absolute HTTP(S) URLs are supported")
    host = parsed.hostname
    try:
        addresses = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError("Unable to resolve URL host") from exc
    for item in addresses:
        address = ip_address(item[4][0])
        if address.is_private or address.is_loopback or address.is_link_local or address.is_reserved or address.is_multicast:
            raise ValueError("URL resolves to a blocked network address")
    return url
