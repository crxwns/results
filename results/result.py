from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, Union

T = TypeVar("T")
E = TypeVar("E", bound=Exception)


class Mixin(ABC, Generic[T, E]):
    @abstractmethod
    def unwrap(self) -> T: ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T: ...

    @abstractmethod
    def unwrap_or_else(self, op: Callable[[E], T]) -> T: ...


@dataclass(frozen=True)
class Ok(Mixin[T, E]):
    _value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def err(self) -> None:
        return None

    def ok(self) -> T:
        return self._value

    def unwrap(self) -> T:
        return self.ok()

    def unwrap_or(self, default: T) -> T:  # noqa: ARG002
        return self.ok()

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:  # noqa: ARG002
        return self.ok()


@dataclass(frozen=True)
class Err(Mixin[T, E]):
    _error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def err(self) -> E:
        return self._error

    def unwrap(self) -> T:
        raise self.err()

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return op(self.err())


Result = Union[Ok[T, E], Err[T, E]]
