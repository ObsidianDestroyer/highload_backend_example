# pylint: disable=redefined-outer-name
import os
import typing as t

import pytest

from backend.src.utils.env import env_or_exit

ENV_NAME = 'ENV_NAME'


@pytest.fixture
def str_env() -> str:
    env_value = 'env_value'
    os.environ[ENV_NAME]: str = env_value

    return env_value


@pytest.fixture
def bool_env() -> bool:
    env_value = 'true'
    os.environ[ENV_NAME]: t.Union[str, bool] = env_value

    return True


def test_env_or_exit_with_unexist_env() -> None:
    env_name = 'NO_SUCH_ENV'

    with pytest.raises(SystemExit) as exc:
        env_or_exit(env_name)

    assert f'You should set \'{env_name}\' env' in str(exc.value)


def test_env_or_exit_with_default_cast(str_env) -> None:
    assert env_or_exit(ENV_NAME) == str_env


def test_env_or_exit_with_bool_cast(bool_env) -> None:
    assert env_or_exit(ENV_NAME, cast=bool) is bool_env


def test_env_or_exit_with_bool_cast_and_invalid_value(str_env) -> None:
    with pytest.raises(SystemExit) as exc:
        env_or_exit(ENV_NAME, bool)

    assert f'\'{ENV_NAME}\' value \'{str_env}\' ' f'is not a boolean' in str(
        exc.value
    )


def test_env_or_exit_with_casting_fail(str_env) -> None:
    with pytest.raises(SystemExit) as exc:
        env_or_exit(ENV_NAME, int)

    assert (
        f'Attempt to cast \'{ENV_NAME}\' value '
        f'\'{str_env}\' to \'int\' failed' in str(exc.value)
    )
