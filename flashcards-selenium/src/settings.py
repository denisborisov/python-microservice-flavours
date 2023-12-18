"""App configuration."""

import pydantic
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_translator_url: pydantic.HttpUrl = pydantic.Field(default="")
    web_scraper_timeout: int = pydantic.Field(default="")

    dictionary_link_css_selector: str = pydantic.Field(default="")
    button_css_selector: str = pydantic.Field(default="")
    definition_css_selector: str = pydantic.Field(default="")
    synonym_css_selector: str = pydantic.Field(default="")
    translation_css_selector: str = pydantic.Field(default="")
    example_css_selector: str = pydantic.Field(default="")

    postgres_dsn: str = pydantic.Field(default="")


AppSettings = Settings()
