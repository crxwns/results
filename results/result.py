from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, Union

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E", bound=Exception)


class _ResultMixin(ABC, Generic[T, E]):
    @abstractmethod
    def expect(self, msg: str) -> T: ...

    @abstractmethod
    def unwrap(self) -> T: ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T: ...

    @abstractmethod
    def unwrap_or_else(self, op: Callable[[E], T]) -> T: ...


@dataclass(frozen=True)
class Ok(_ResultMixin[T, E]):
    _value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def err(self) -> None:
        return None

    def ok(self) -> T:
        return self._value

    def expect(self, msg: str) -> T:
        return self.ok()

    def unwrap(self) -> T:
        return self.ok()

    def unwrap_or(self, default: T) -> T:
        return self.ok()

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return self.ok()


@dataclass(frozen=True)
class Err(_ResultMixin[T, E]):
    _error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def err(self) -> E:
        return self._error

    def ok(self) -> None:
        return None

    def expect(self, msg: str) -> T:
        err = self.err()
        err.add_note(msg)
        raise err

    def unwrap(self) -> T:
        raise self.err()

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return op(self.err())


Result = Union[Ok[T, E], Err[T, E]]


class _OptionMixin(ABC, Generic[T]):
    @abstractmethod
    def expect(self, msg: str) -> T: ...

    @abstractmethod
    def unwrap(self) -> T: ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T: ...

    @abstractmethod
    def unwrap_or_else(self, op: Callable[[], T]) -> T: ...

    @abstractmethod
    def map(self, op: Callable[[T], U]) -> "Option[U]": ...

    @abstractmethod
    def inspect(self, op: Callable[[T], Any]) -> "Option[T]": ...

    @abstractmethod
    def filter(self, op: Callable[[T], bool]) -> "Option[T]": ...


@dataclass(frozen=True)
class Some(_OptionMixin[T]):
    _value: T

    def is_some(self) -> bool:
        return True

    def is_none(self) -> bool:
        return False

    def some(self) -> T:
        return self._value

    def is_some_and(self, op: Callable[[T], bool]) -> bool:
        return op(self.some())

    def expect(self, msg: str) -> T:
        return self.some()

    def unwrap(self) -> T:
        return self.some()

    def unwrap_or(self, default: T) -> T:
        return self.some()

    def unwrap_or_else(self, op: Callable[[], T]) -> T:
        return self.some()

    def map(self, op: Callable[[T], U]) -> "Option[U]":
        return Some(op(self.some()))

    def inspect(self, op: Callable[[T], Any]) -> "Option[T]":
        op(self.some())
        return self

    def filter(self, op: Callable[[T], bool]) -> "Option[T]":
        if op(self.some()):
            return self
        return NONE()


@dataclass(frozen=True)
class NONE(_OptionMixin[T]):
    def is_some(self) -> bool:
        return False

    def is_none(self) -> bool:
        return True

    def is_some_and(self, op: Callable[[T], bool]) -> bool:
        return False

    def expect(self, msg: str) -> T:
        raise ValueError(msg)

    def unwrap(self) -> T:
        raise ValueError("Value is None.")

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: Callable[[], T]) -> T:
        return op()

    def map(self, op: Callable[[T], U]) -> "Option[U]":
        return self

    def inspect(self, op: Callable[[T], Any]) -> "Option[T]":
        return self

    def filter(self, op: Callable[[T], bool]) -> "Option[T]":
        return self


Option = Union[Some[T], NONE]
