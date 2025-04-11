import os

import pytest

from src.config import get_env


@pytest.mark.parametrize("default_value", ["default_value", 42, 3.14, True, False])
def test_get_env_default(default_value):
    """
    GIVEN an environment variable 'NON_EXISTENT_VAR' that is not set
    WHEN 'get_env' is called with a default value 'default_value'
    THEN it should return 'default_value'
    """
    assert get_env("NON_EXISTENT_VAR", default=default_value) == default_value


def test_get_env_cast_int():
    """
    GIVEN an environment variable 'TEST_INT_VAR' set to '42'
    WHEN 'get_env' is called with 'cast=int'
    THEN it should return the integer 42
    """
    os.environ["TEST_INT_VAR"] = "42"
    assert get_env("TEST_INT_VAR", cast=int) == 42


def test_get_env_cast_float():
    """
    GIVEN an environment variable 'TEST_FLOAT_VAR' set to '3.14'
    WHEN 'get_env' is called with 'cast=float'
    THEN it should return the float 3.14
    """
    os.environ["TEST_FLOAT_VAR"] = "3.14"
    assert get_env("TEST_FLOAT_VAR", cast=float) == 3.14


@pytest.mark.parametrize(
    ("env_var_value", "expected_value"),
    [("1", True), ("0", False), ("true", True), ("false", False), ("yes", True), ("no", False)],
)
def test_get_env_cast_bool(env_var_value, expected_value):
    """
    GIVEN an environment variable 'TEST_BOOL_VAR' set to <var_value>
    WHEN 'get_env' is called with 'cast=bool'
    THEN it should return boolean value <expected_value>

    Examples:
        | var_value |     expected_value |
        |       "1" |               True |
        |       "0" |              False |


    """
    os.environ["TEST_BOOL_VAR"] = env_var_value
    result = get_env("TEST_BOOL_VAR", cast=bool)
    assert isinstance(result, bool)
    assert result == expected_value


def test_get_env_cast_invalid():
    """
    GIVEN an environment variable 'TEST_INVALID_CAST' set to 'not_a_number'
    WHEN 'get_env' is called with 'cast=int'
    THEN it should raise a 'ValueError'
    """
    os.environ["TEST_INVALID_CAST"] = "not_a_number"
    with pytest.raises(ValueError, match="invalid literal for int()"):
        get_env("TEST_INVALID_CAST", cast=int)


def test_get_env_min_value():
    """
    GIVEN an environment variable 'TEST_MIN_VAR' set to '5'
    WHEN 'get_env' is called with 'cast=int' and 'num_min=10'
    THEN it should return the minimum value 10
    """
    os.environ["TEST_MIN_VAR"] = "5"
    assert get_env("TEST_MIN_VAR", cast=int, num_min=10) == 10


def test_get_env_max_value():
    """
    GIVEN an environment variable 'TEST_MAX_VAR' set to '50'
    WHEN 'get_env' is called with 'cast=int' and 'num_max=40'
    THEN it should return the maximum value 40
    """
    os.environ["TEST_MAX_VAR"] = "50"
    assert get_env("TEST_MAX_VAR", cast=int, num_max=40) == 40


def test_get_env_min_max_within_range():
    """
    GIVEN an environment variable 'TEST_RANGE_VAR' set to '25'
    WHEN 'get_env' is called with 'cast=int', 'num_min=10', and 'num_max=40'
    THEN it should return the value 25 as it is within the range
    """
    os.environ["TEST_RANGE_VAR"] = "25"
    assert get_env("TEST_RANGE_VAR", cast=int, num_min=10, num_max=40) == 25


def test_get_env_no_cast():
    """
    GIVEN an environment variable 'TEST_NO_CAST' set to 'some_value'
    WHEN 'get_env' is called without a 'cast'
    THEN it should return the string 'some_value'
    """
    os.environ["TEST_NO_CAST"] = "some_value"
    assert get_env("TEST_NO_CAST") == "some_value"


def test_empty_env_var():
    """
    GIVEN an environment variable 'EMPTY_VAR' set to an empty string
    WHEN 'get_env' is called with 'default_value'
    THEN it should return an empty string

    NOTE: This test is to check the behavior when the environment variable is set but empty.
    """
    os.environ["EMPTY_VAR"] = ""
    assert get_env("EMPTY_VAR", default="default_value") == ""
