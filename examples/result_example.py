from results import Err, Ok, Result

number = int | float


def division(dividend: number, divisor: number) -> Result[number, Exception]:
    if divisor == 0:
        return Err(ZeroDivisionError("Cannot divide by 0."))

    return Ok(dividend / divisor)


def output_error(error: Exception) -> None:
    print(f"Encountered {type(error).__name__}: {error}")


if __name__ == "__main__":
    print("---\nSince python 3.10 you can use the match-case syntax to match on the result")

    match division(dividend=10, divisor=2):
        case Ok(value):
            print(value)
        case Err(e):
            output_error(e)

    print("---")

    print("Or use isinstance to check for Err or Ok")

    division_result = division(dividend=10, divisor=0)
    if isinstance(division_result, Err):
        output_error(division_result.err())

    print("---")

    print("Or check if result.is_ok() / result.is_err()")

    is_err = division_result.is_err()
    print(f"is_err?: {is_err}")

    print("---")

    print("Use unwrap to raise the exception on Err")

    try:
        division_result.unwrap()
    except ZeroDivisionError as e:
        print("Catched Error", end=None)
        output_error(e)

    print("---")

    print("Use unwrap_or to use a default value")

    unwrap_or = division_result.unwrap_or(0)
    print(f"unwrap_or(): {unwrap_or}")

    print("---")

    print("use unwrap_or_else to use a Callable[[E], T] taking in the exception and returning <T>")

    unwrap_or_else = division_result.unwrap_or_else(lambda x: 2)
    print(f"unwrap_or_else(): {unwrap_or_else}")

    print("---")
