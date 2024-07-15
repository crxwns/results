import pytest

from results import Err, Ok, Result
from results.option import Some


def return_err_result() -> Result[None, Exception]:
    return Err(ValueError("ValueError"))


def return_ok_result() -> Result[int, Exception]:
    return Ok(1)


def test_err_result() -> None:
    result = return_err_result()

    assert result.is_err()
    assert not result.is_ok()
    assert isinstance(result, Err)
    assert isinstance(result.err().unwrap(), ValueError)
    assert isinstance(result.err(), Some)


def test_ok_result() -> None:
    result = return_ok_result()

    assert result.is_ok()
    assert not result.is_err()
    assert isinstance(result, Ok)
    assert isinstance(result.ok().unwrap(), int)
    assert isinstance(result.ok(), Some)


def test_match_error() -> None:
    match return_err_result():
        case Err(e):
            assert True
            assert isinstance(e, ValueError)
        case Ok():
            pytest.fail("Shouldn't match Ok()")


def test_match_ok() -> None:
    match return_ok_result():
        case Err():
            pytest.fail("Shouldn't match Err()")
        case Ok(value):
            assert True
            assert isinstance(value, int)


def test_equality() -> None:
    exc = Exception("Hi")
    assert Err(exc) == Err(exc)
    assert Err(Exception("Hi")) != Err(Exception("Hi"))
    assert Ok(1) == Ok(1)
    assert Ok(1) != Ok(2)
    assert Ok(exc) != Err(exc)  # type: ignore[comparison-overlap]


def double(value: int) -> int:
    return value * 2


def test_map() -> None:
    assert isinstance(Ok(5).map(double), Ok)
    assert isinstance(Err(Exception("Hi")).map(double), Err)
    assert isinstance(Ok(2).map(double).map(lambda x: x * 10), Ok)


def intify(value: str) -> Result[int, ValueError]:
    try:
        return Ok(int(value))
    except ValueError as e:
        return Err(e)


def test_and_then() -> None:
    assert isinstance(Ok("5").and_then(intify), Ok)
    assert isinstance(Ok("5").and_then(intify).map(lambda x: x * 5), Ok)
    assert isinstance(Ok("a").and_then(intify), Err)
