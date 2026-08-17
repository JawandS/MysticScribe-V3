"""Typed application configuration loaded from the environment."""

from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import AnyHttpUrl, BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelRoutingSettings(BaseModel):
    """Provider-neutral routes served by the configured LiteLLM proxy."""

    base_url: AnyHttpUrl = AnyHttpUrl("http://127.0.0.1:4000/v1")
    actor_model: str = "mysticscribe-character"
    adjudicator_model: str = "mysticscribe-adjudicator"
    api_key: SecretStr | None = None


class RunLengthSettings(BaseModel):
    """Limits that stop a simulation run cleanly."""

    round_limit: Annotated[int, Field(ge=1)] = 3
    turn_limit: Annotated[int, Field(ge=1)] | None = None


class Settings(BaseSettings):
    """Validated runtime settings with safe local defaults."""

    model_config = SettingsConfigDict(
        env_prefix="MYSTICSCRIBE_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    model: ModelRoutingSettings = Field(default_factory=ModelRoutingSettings)
    database_path: Path = Path("data/mysticscribe.sqlite3")
    seed: Annotated[int, Field(ge=0)] = 0
    retry_limit: Annotated[int, Field(ge=0, le=10)] = 3
    run_length: RunLengthSettings = Field(default_factory=RunLengthSettings)


@lru_cache
def get_settings() -> Settings:
    """Return one immutable-by-convention settings instance per process."""

    return Settings()
