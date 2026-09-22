# Security model

The baseline rejects oversized inputs and provides PII redaction helpers. Production deployments should add authentication, authorization, request signing, secret management, SSRF-safe URL fetching, content sandboxing, audit logs, rate limits, and model prompt-injection defenses before accepting untrusted web sources.
