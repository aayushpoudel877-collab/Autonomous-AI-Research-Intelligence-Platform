def validate_text_size(text: str, max_chars: int) -> None:
    if len(text) > max_chars:
        raise ValueError(f"text exceeds {max_chars} characters")


def validate_bytes_size(payload: bytes, max_bytes: int) -> None:
    if len(payload) > max_bytes:
        raise ValueError(f"payload exceeds {max_bytes} bytes")
