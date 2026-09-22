class PlatformError(Exception):
    """Base exception for extended platform services."""

class ValidationError(PlatformError):
    """Raised when a research input violates a contract."""

class DependencyError(PlatformError):
    """Raised when an optional provider is unavailable."""
