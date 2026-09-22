from nexus.security.redaction import redact

def test_email_redaction(): assert 'a@example.com' not in redact('contact a@example.com')
