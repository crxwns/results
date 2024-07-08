from results import NONE, Option, Some


def division(dividend: float, divisor: float) -> Option[float]:
    if divisor == 0:
        return NONE()

    return Some(dividend / divisor)


# Create a Some and a NONE
division_option_some = division(dividend=10, divisor=2)
division_option_none = division(dividend=10, divisor=0)

# Bool if Option is NONE or Some
print(f"is_none: {division_option_some.is_none()}")
print(f"is_some: {division_option_some.is_some()}")

# If Option is Some and condition is True returns bool
print(f"is_some_and: {division_option_some.is_some_and(lambda x: x < 2)}")
print(f"is_some_and: {division_option_some.is_some_and(lambda x: x > 0)}")

# Unwraps Option and returns Some if Some else raises ValueError if NONE
print(f"unwrap: {division_option_some.unwrap()}")
try:
    division_option_none.unwrap()
except ValueError as e:
    print(f"Option was NONE: {e}")

# Unwraps Option and uses default if NONE
print(f"unwrap_or some: {division_option_some.unwrap_or(0)}")
print(f"unwrap_or none: {division_option_none.unwrap_or(2)}")

# Unwraps Option and calls Callable[[], T] if NONE
print(f"unwrap_or_else some: {division_option_some.unwrap_or_else(lambda: 50)}")
print(f"unwrap_or_else none: {division_option_none.unwrap_or_else(lambda: 50)}")

# Match on Option
match division(dividend=5, divisor=1):
    case Some(value):
        print(f"Matched Some: {value}")
    case NONE():
        print("There's nothing.")


# Map Option to a Callable[[T], U] which can be chained
def list_option_some() -> Option[list[int]]:
    return Some([1, 2, 3, 4, 5])


def list_sum(inp: list[int]) -> int:
    return sum(inp)


list_option = list_option_some()
print(list_option.map(list_sum).map(lambda x: x * 2).unwrap_or(0))


# Run Callable[[T], Any] when Some and return original Option
print(list_option.inspect(lambda x: print(f"Hi {x[1]}")).unwrap())

# Run Callable[[T], bool] to check if condition is met and return Some if True or NONE if False
print(division_option_some.filter(lambda x: x % 2 != 0).unwrap())
