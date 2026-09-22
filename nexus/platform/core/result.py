from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

@dataclass(frozen=True)
class Result(Generic[T]):
    value: T | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None

    @classmethod
    def success(cls, value: T) -> "Result[T]":
        return cls(value=value)

    @classmethod
    def failure(cls, error: str) -> "Result[T]":
        return cls(error=error)
