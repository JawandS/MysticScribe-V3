"""Tests for application settings."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from mysticscribe.config import Settings

_SETTINGS_ENV_VARS = (
    "MYSTICSCRIBE_MODEL",
    "MYSTICSCRIBE_MODEL__ACTOR_MODEL",
    "MYSTICSCRIBE_MODEL__ADJUDICATOR_MODEL",
    "MYSTICSCRIBE_MODEL__BASE_URL",
    "MYSTICSCRIBE_MODEL__API_KEY",
    "MYSTICSCRIBE_DATABASE_PATH",
    "MYSTICSCRIBE_SEED",
    "MYSTICSCRIBE_RETRY_LIMIT",
    "MYSTICSCRIBE_RUN_LENGTH",
    "MYSTICSCRIBE_RUN_LENGTH__ROUND_LIMIT",
    "MYSTICSCRIBE_RUN_LENGTH__TURN_LIMIT",
)


@pytest.fixture(autouse=True)
def clear_settings_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for variable in _SETTINGS_ENV_VARS:
        monkeypatch.delenv(variable, raising=False)


def test_settings_have_safe_local_defaults() -> None:
    settings = Settings()

    assert settings.database_path == Path("data/mysticscribe.sqlite3")
    assert settings.seed == 0
    assert settings.retry_limit == 3
    assert settings.run_length.round_limit == 3
    assert settings.run_length.turn_limit is None
    assert settings.model.actor_model == "mysticscribe-character"


def test_settings_load_nested_environment_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MYSTICSCRIBE_MODEL__ACTOR_MODEL", "local-character")
    monkeypatch.setenv("MYSTICSCRIBE_RUN_LENGTH__ROUND_LIMIT", "5")
    monkeypatch.setenv("MYSTICSCRIBE_DATABASE_PATH", "tmp/world.sqlite3")

    settings = Settings()

    assert settings.model.actor_model == "local-character"
    assert settings.run_length.round_limit == 5
    assert settings.database_path == Path("tmp/world.sqlite3")


def test_settings_reject_invalid_limits() -> None:
    with pytest.raises(ValidationError):
        Settings(retry_limit=11)
