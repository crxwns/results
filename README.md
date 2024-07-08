# Results

Implementation of Rust's Result- and Option-Type in Python.

Can be used to mimic similar behaviour as Rust to propagate Exceptions to the caller instead of handling them in the method itself and use default values if there is an `Error` or the `Option` is `None`.

```python
from dataclasses import dataclass

import tomllib

from results import Err, Ok, Result


@dataclass
class Config:
    debug: bool
    value: int


def parse_config_from_toml_string(config_str: str) -> Result[Config, Exception]:
    """Takes in a TOML string and returns a Result[Config, Exception]"""
    try:
        data = tomllib.loads(config_str)
    except tomllib.TOMLDecodeError as e:
        return Err(e)

    tool = data.get("tool")

    if not tool:
        return Err(ValueError("No configuration for tool in config."))

    try:
        config = Config(**tool)
    except ValueError as e:
        return Err(e)

    return Ok(config)


if __name__ == "__main__":
    valid_config_str = """[tool]
    debug = true
    value = 10"""

    invalid_config_str = """[wrong]
    debug = true
    value = 10"""

    valid_config_result = parse_config_from_toml_string(config_str=valid_config_str)
    invalid_config_result = parse_config_from_toml_string(config_str=invalid_config_str)

    # You can match on the result

    match valid_config_result:
        case Err(err):
            print(err)
        case Ok(config):
            print(config)

    # Use a default for the config if Err

    print(invalid_config_result.unwrap_or(Config(debug=False, value=2)))

```

# Examples

- [Option[T]](examples/option_example.py)
- [Result[T, E]](examples/result_example.py)
