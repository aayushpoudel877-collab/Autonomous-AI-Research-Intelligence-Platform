import pytest

from nexus.security.limits import validate_bytes_size, validate_text_size


def test_text_limit():
    with pytest.raises(ValueError):
        validate_text_size("abcd", 3)


def test_byte_limit():
    with pytest.raises(ValueError):
        validate_bytes_size(b"abcd", 3)
