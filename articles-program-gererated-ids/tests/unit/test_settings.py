"""Unit tests related to environment variables."""

import os

from src.settings import AppSettings


class TestEnvironmentVariables:
    def test_environment_variables_exist(self) -> None:
        assert os.environ.get("POSTGRES_DSN")


class TestSettings:
    def test_app_settings_initialized(self) -> None:
        assert AppSettings.postgres_dsn

    def test_all_app_settings_has_been_considered(self) -> None:
        assert len(AppSettings.model_dump()) == 1
