from dataclasses import dataclass

@dataclass(frozen=True)
class ResourceLimits:
    max_documents: int = 10_000
    max_chunks_per_document: int = 500
    max_context_tokens: int = 8_000

    def validate(self) -> None:
        if min(self.max_documents, self.max_chunks_per_document, self.max_context_tokens) <= 0:
            raise ValueError("resource limits must be positive")
