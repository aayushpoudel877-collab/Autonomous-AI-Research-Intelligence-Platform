import pytest

from nexus.ingestion.web import _HTMLTextParser
from nexus.security.url_policy import validate_url


def test_html_parser_ignores_script_and_style():
    parser = _HTMLTextParser()
    parser.feed("<h1>Research</h1><script>ignore()</script><p>Evidence</p><style>x{}</style>")
    assert parser.parts == ["Research", "Evidence"]


def test_private_ip_is_rejected():
    with pytest.raises(ValueError, match="blocked"):
        validate_url("http://127.0.0.1:8000/internal")
