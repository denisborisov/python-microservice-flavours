"""Unit tests related to environment variables."""

import os

from src.settings import AppSettings


class TestEnvironmentVariables:
    def test_environment_variables_exist(self) -> None:
        assert os.environ.get("GOOGLE_TRANSLATOR_URL")
        assert os.environ.get("WEB_SCRAPER_TIMEOUT")

        assert os.environ.get("DICTIONARY_LINK_CSS_SELECTOR")
        assert os.environ.get("BUTTON_CSS_SELECTOR")
        assert os.environ.get("DEFINITION_CSS_SELECTOR")
        assert os.environ.get("SYNONYM_CSS_SELECTOR")
        assert os.environ.get("TRANSLATION_CSS_SELECTOR")
        assert os.environ.get("EXAMPLE_CSS_SELECTOR")

        assert os.environ.get("POSTGRES_DSN")


class TestSettings:
    def test_app_settings_initialized(self) -> None:
        assert AppSettings.google_translator_url
        assert AppSettings.web_scraper_timeout

        assert AppSettings.dictionary_link_css_selector
        assert AppSettings.button_css_selector
        assert AppSettings.definition_css_selector
        assert AppSettings.synonym_css_selector
        assert AppSettings.translation_css_selector
        assert AppSettings.example_css_selector

        assert AppSettings.postgres_dsn
