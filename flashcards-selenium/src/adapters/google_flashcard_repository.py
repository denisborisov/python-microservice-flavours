"""Flashcard repository."""

import typing

import dependency_injector.wiring
from pydantic import HttpUrl

from ..containers.web_scraper import WebScraperContainer
from ..domain.exceptions import WebScraperError
from ..domain.model import Flashcard
from ..services.web_scraper import AbstractWebScraper
from ..settings import AppSettings


class AbstractGoogleFlashcardRepository(typing.Protocol):
    seen: set[Flashcard]

    def retrieve_flashcard_by_word(self, word: str) -> Flashcard | None:
        flashcard = self._retrieve_flashcard_by_word(word)
        if flashcard:
            self.seen.add(flashcard)
        return flashcard

    def _retrieve_flashcard_by_word(self, word: str) -> Flashcard | None:
        raise NotImplementedError


class GoogleFlashcardRepository(AbstractGoogleFlashcardRepository):
    def __init__(
        self,
        web_scraper: AbstractWebScraper = dependency_injector.wiring.Provide[
            WebScraperContainer.web_scraper,
        ],
    ) -> None:
        self.web_scraper = web_scraper
        self.seen: set[Flashcard] = set()

    def _retrieve_flashcard_by_word(self, word: str) -> Flashcard | None:
        url: HttpUrl = HttpUrl(f"{AppSettings.google_translator_url.unicode_string()}{word}")
        with self.web_scraper:
            self.web_scraper.load_web_page(url)
            if self.web_scraper.check_dictionary_availability():
                try:
                    buttons = self.web_scraper.find_all_elements_by_css_selector(
                        AppSettings.button_css_selector,
                    )
                except WebScraperError:
                    buttons = []
                else:
                    for button in buttons:
                        self.web_scraper.press_a_button(button)

                try:
                    definitions = self.web_scraper.extract_text_from_elements(
                        AppSettings.definition_css_selector,
                    )
                except WebScraperError:
                    definitions = []

                try:
                    synonyms = self.web_scraper.extract_text_from_elements(
                        AppSettings.synonym_css_selector,
                    )
                except WebScraperError:
                    synonyms = []

                try:
                    translations = self.web_scraper.extract_text_from_elements(
                        AppSettings.translation_css_selector,
                    )
                except WebScraperError:
                    translations = []

                try:
                    examples = self.web_scraper.extract_text_from_elements(
                        AppSettings.example_css_selector,
                    )
                except WebScraperError:
                    examples = []

                return Flashcard(word, definitions, synonyms, translations, examples)
        return None
