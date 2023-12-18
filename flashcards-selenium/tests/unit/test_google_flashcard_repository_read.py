"""Integration tests related to Google flashcard repository's READ operations."""

from .. import conftest
from src.adapters.google_flashcard_repository import GoogleFlashcardRepository


class TestRetrieveFlashcardByWord:
    def test_can_retrieve_flashcard_by_word(self) -> None:
        web_scraper: conftest.FakeWebScraper = conftest.FakeWebScraper()
        google_repo = GoogleFlashcardRepository(web_scraper=web_scraper)

        retrieved_flashcard = google_repo.retrieve_flashcard_by_word("WORD")

        assert retrieved_flashcard
        assert retrieved_flashcard in google_repo.seen
        assert web_scraper.web_page_loaded
        assert web_scraper.is_dictionary_available
        assert web_scraper.number_of_buttons_pressed == 2  # noqa: PLR2004

    def test_cannot_retrieve_flashcard_by_word_if_dictionary_unavailable(self) -> None:
        web_scraper: conftest.FakeWebScraper = conftest.FakeWebScraper()
        google_repo = GoogleFlashcardRepository(web_scraper=web_scraper)

        retrieved_flashcard = google_repo.retrieve_flashcard_by_word("NO_SUCH_WORD")

        assert not retrieved_flashcard
        assert web_scraper.web_page_loaded
        assert not web_scraper.is_dictionary_available
        assert not web_scraper.number_of_buttons_pressed
