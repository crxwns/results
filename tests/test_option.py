import pytest

from results import NONE, Some


def test_some_option() -> None:
    assert Some(1).is_some()
    assert not Some(1).is_none()
    assert Some(1).expect("Is some") == 1
    assert Some(1).is_some_and(lambda x: x == 1)
    assert Some(1).inspect(lambda x: None).unwrap()
    assert Some(1).filter(lambda x: x != 1).is_none()
    assert Some(1).filter(lambda x: x == 1).is_some()
    assert Some(1).map(lambda x: x * 2).is_some_and(lambda x: x == 2)
    assert Some(1).unwrap() == 1
    assert Some(1).unwrap_or(0) == 1
    assert Some(1).unwrap_or_else(lambda: 0) == 1


def test_none_option() -> None:
    assert not NONE().is_some()
    assert NONE().is_none()
    with pytest.raises(ValueError, match="Is some"):
        NONE().expect("Is some")
    assert not NONE().is_some_and(lambda x: x == 1)
    NONE().inspect(lambda x: pytest.fail("Shouldn't be here."))
    assert NONE().filter(lambda x: x != 1).is_none()
    assert NONE().filter(lambda x: x == 1).is_none()
    assert NONE().map(lambda x: pytest.fail("Shouldn't be here.")).is_none()  # type: ignore[misc]
    with pytest.raises(ValueError, match="Value is None."):
        NONE().unwrap()
    assert NONE[int]().unwrap_or(0) == 0
    assert NONE[int]().unwrap_or_else(lambda: 0) == 0
