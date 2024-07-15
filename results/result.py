from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, Union

from results.option import NONE, Option, Some

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E", bound=Exception)


class _ResultMixin(ABC, Generic[T, E]):
    @abstractmethod
    def is_ok(self) -> bool: ...

    @abstractmethod
    def is_err(self) -> bool: ...

    @abstractmethod
    def is_ok_and(self, op: Callable[[T], bool]) -> bool: ...

    @abstractmethod
    def is_err_and(self, op: Callable[[E], bool]) -> bool: ...

    @abstractmethod
    def expect(self, msg: str) -> T: ...

    @abstractmethod
    def unwrap(self) -> T: ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T: ...

    @abstractmethod
    def unwrap_or_else(self, op: Callable[[E], T]) -> T: ...

    @abstractmethod
    def err(self) -> Option[E]: ...

    @abstractmethod
    def ok(self) -> Option[T]: ...

    @abstractmethod
    def map(self, op: Callable[[T], U]) -> "Result[U, E]": ...

    @abstractmethod
    def and_then(self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]": ...


@dataclass(frozen=True)
class Ok(_ResultMixin[T, E]):
    _value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def is_ok_and(self, op: Callable[[T], bool]) -> bool:
        return op(self._value)

    def is_err_and(self, op: Callable[[E], bool]) -> bool:
        return False

    def err(self) -> Option[E]:
        return NONE()

    def ok(self) -> Option[T]:
        return Some(self._value)

    def expect(self, msg: str) -> T:
        return self._value

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return self._value

    def map(self, op: Callable[[T], U]) -> "Result[U, E]":
        return Ok(op(self._value))

    def and_then(self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        return op(self._value)


@dataclass(frozen=True)
class Err(_ResultMixin[T, E]):
    _error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def is_ok_and(self, op: Callable[[T], bool]) -> bool:
        return False

    def is_err_and(self, op: Callable[[E], bool]) -> bool:
        return op(self._error)

    def err(self) -> Option[E]:
        return Some(self._error)

    def ok(self) -> Option[T]:
        return NONE()

    def expect(self, msg: str) -> T:
        err = self._error
        err.add_note(msg)
        raise err

    def unwrap(self) -> T:
        raise self._error

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return op(self._error)

    def map(self, op: Callable[[T], U]) -> "Result[U, E]":
        return Err(self._error)

    def and_then(self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        return Err(self._error)


Result = Union[Ok[T, E], Err[T, E]]
