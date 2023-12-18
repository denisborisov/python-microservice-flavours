"""Integration tests related to web scraper."""

import pytest

from pydantic import HttpUrl

from src.domain.exceptions import WebScraperError
from src.services.web_scraper import SeleniumWebScraper
from src.settings import AppSettings


class TestWebScraper:
    def test_raises_exceptions_on_invalid_page(self) -> None:
        invalid_url = HttpUrl("http://www.no_such_url.com")

        with pytest.raises(WebScraperError), SeleniumWebScraper() as web_scraper:
            web_scraper.load_web_page(invalid_url)

    def test_page_contains_dictionary_for_known_word(self) -> None:
        url: HttpUrl = HttpUrl(f"{AppSettings.google_translator_url.unicode_string()}cup")
        with SeleniumWebScraper() as web_scraper:
            web_scraper.load_web_page(url)

            assert web_scraper.check_dictionary_availability()

    def test_page_does_not_contains_dictionary_for_unknown_word(self) -> None:
        url: HttpUrl = HttpUrl(f"{AppSettings.google_translator_url.unicode_string()}ABCDZYXW")
        with SeleniumWebScraper() as web_scraper:
            web_scraper.load_web_page(url)

            assert not web_scraper.check_dictionary_availability()

    def test_can_find_buttons_by_css_selector(self) -> None:
        url: HttpUrl = HttpUrl(f"{AppSettings.google_translator_url.unicode_string()}cup")
        with SeleniumWebScraper() as web_scraper:
            web_scraper.load_web_page(url)
            buttons = web_scraper.find_all_elements_by_css_selector(
                AppSettings.button_css_selector,
            )

            assert buttons

    def test_raises_exception_when_cannot_find_buttons_for_unknown_word(self) -> None:
        url: HttpUrl = HttpUrl(f"{AppSettings.google_translator_url.unicode_string()}ABCDZYXW")
        with SeleniumWebScraper() as web_scraper:
            web_scraper.load_web_page(url)

            with pytest.raises(WebScraperError):
                web_scraper.find_all_elements_by_css_selector(
                    AppSettings.button_css_selector,
                )

    def test_raises_exception_when_cannot_press_buttons_for_unknown_word(self) -> None:
        url: HttpUrl = HttpUrl(f"{AppSettings.google_translator_url.unicode_string()}ABCDZYXW")
        with SeleniumWebScraper() as web_scraper:
            web_scraper.load_web_page(url)

            with pytest.raises(WebScraperError):
                web_scraper.press_a_button(
                    AppSettings.button_css_selector,
                )

    def test_can_extract_text_from_elements(self) -> None:
        url: HttpUrl = HttpUrl(f"{AppSettings.google_translator_url.unicode_string()}cup")
        with SeleniumWebScraper() as web_scraper:
            web_scraper.load_web_page(url)

            buttons = web_scraper.find_all_elements_by_css_selector(
                AppSettings.button_css_selector,
            )
            for button in buttons:
                web_scraper.press_a_button(button)

            synonyms = web_scraper.extract_text_from_elements(
                AppSettings.synonym_css_selector,
            )

            assert synonyms == [
                "trophy",
                "chalice",
                "award",
                "prize",
                "punch",
                "drink",
                "mixed drink",
            ]

    def test_raises_exceptions_when_cannot_extract_text_for_unknown_word(self) -> None:
        url: HttpUrl = HttpUrl(f"{AppSettings.google_translator_url.unicode_string()}ABCDZYXW")
        with SeleniumWebScraper() as web_scraper:
            web_scraper.load_web_page(url)

            with pytest.raises(WebScraperError):
                web_scraper.extract_text_from_elements(
                    AppSettings.synonym_css_selector,
                )
