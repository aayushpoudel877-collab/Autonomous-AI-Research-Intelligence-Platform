from nexus.ingestion.web import _HTMLTextParser


def test_html_parser_ignores_script_and_style():
    parser = _HTMLTextParser()
    parser.feed("<h1>Research</h1><script>ignore()</script><p>Evidence</p><style>x{}</style>")
    assert parser.parts == ["Research", "Evidence"]
