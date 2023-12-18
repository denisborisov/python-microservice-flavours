"""General fixtures."""

import types
import typing
import typing_extensions

from pydantic import HttpUrl
import pytest
import sqlalchemy.ext.asyncio

from src.adapters.local_flashcard_repository import SqlAlchemyFlashcardRepository
from src.adapters import google_flashcard_repository
from src.adapters.orm import Base
from src.domain.messages import Message
from src.domain.model import Flashcard
from src.services import unit_of_work
from src.services.web_scraper import AbstractWebScraper
from src.services.message_bus import MessageBus


class FakeWebScraper(AbstractWebScraper):
    def __init__(self) -> None:
        self.number_of_buttons_pressed = 0

    def __enter__(self) -> typing_extensions.Self:
        return super().__enter__()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        return super().__exit__(exc_type, exc_val, exc_tb)

    def _load_web_page(self, url: HttpUrl) -> None:
        self.web_page_loaded = True
        self.is_dictionary_available = True
        if url.unicode_string().endswith("NO_SUCH_WORD"):
            self.is_dictionary_available = False

    def _check_dictionary_availability(self) -> bool:
        return self.is_dictionary_available

    def _find_all_elements_by_css_selector(self, css_selector: str) -> list[str]:
        return self._extract_text_from_elements(
            [css_selector] * 2 if css_selector.startswith("button") else [css_selector],
        )

    def _press_a_button(self, button: typing.Any) -> None:  # noqa: ARG002
        self.number_of_buttons_pressed += 1

    def _extract_text_from_elements(self, elements: list[str]) -> list[str]:
        return elements


@pytest.fixture()
def fake_web_scraper() -> AbstractWebScraper:
    return FakeWebScraper()


@pytest.fixture()
def fake_google_flashcard_repository(
    fake_web_scraper: AbstractWebScraper,
) -> google_flashcard_repository.AbstractGoogleFlashcardRepository:
    return google_flashcard_repository.GoogleFlashcardRepository(web_scraper=fake_web_scraper)


@pytest.fixture()
async def in_memory_sqlite_db() -> typing.AsyncGenerator:
    engine = sqlalchemy.ext.asyncio.create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture()
def sqlite_session_factory(
    in_memory_sqlite_db: sqlalchemy.ext.asyncio.AsyncEngine,
) -> sqlalchemy.ext.asyncio.async_sessionmaker:
    return sqlalchemy.ext.asyncio.async_sessionmaker(
        bind=in_memory_sqlite_db,
        expire_on_commit=False,
    )


@pytest.fixture()
def sqlite_uow(
    sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    fake_google_flashcard_repository: google_flashcard_repository.AbstractGoogleFlashcardRepository,  # noqa: E501
) -> unit_of_work.AbstractUnitOfWork:
    return unit_of_work.SqlAlchemyUnitOfWork(
        session_factory=sqlite_session_factory,
        google_flashcard_repository=fake_google_flashcard_repository,
    )


@pytest.fixture()
def sqlite_bus(sqlite_uow: unit_of_work.SqlAlchemyUnitOfWork) -> MessageBus:
    return MessageBus(uow=sqlite_uow)


async def handle(message_bus: MessageBus, message: Message) -> typing.Any:
    message_bus.start_process_events()
    result = await message_bus.handle(message)
    await message_bus.stop_process_events()
    return result


class ServiceClass:
    @staticmethod
    def get_default_flashcard(data: dict) -> Flashcard:
        if definitions_data := data.get("definitions"):
            definitions = [
                f"{data.get('prefix', '')}{one_definition}" for one_definition in definitions_data
            ]
        else:
            definitions = [f"{data.get('prefix', '')}DEFINITION"]
        if synonyms_data := data.get("synonyms"):
            synonyms = [f"{data.get('prefix', '')}{one_synonym}" for one_synonym in synonyms_data]
        else:
            synonyms = [f"{data.get('prefix', '')}SYNONYM"]
        if translations_data := data.get("translations"):
            translations = [
                f"{data.get('prefix', '')}{one_translation}"
                for one_translation in translations_data
            ]
        else:
            translations = [f"{data.get('prefix', '')}TRANSLATION"]
        if examples_data := data.get("examples"):
            examples = [f"{data.get('prefix', '')}{one_example}" for one_example in examples_data]
        else:
            examples = [f"{data.get('prefix', '')}EXAMPLE"]

        return Flashcard(
            word=f"{data.get('prefix', '')}{data.get('word', 'WORD')}",
            definitions=definitions,
            synonyms=synonyms,
            translations=translations,
            examples=examples,
        )

    @staticmethod
    async def create_local_repository_with_flashcards(
        sqlite_uow: unit_of_work.SqlAlchemyUnitOfWork,
        *flashcards_data: dict,
    ) -> tuple[SqlAlchemyFlashcardRepository, list[Flashcard]]:
        local_repo = SqlAlchemyFlashcardRepository(sqlite_uow._session.get())  # noqa: SLF001

        flashcards: list[Flashcard] = []
        for one_dict in flashcards_data:
            one_flashcard = ServiceClass.get_default_flashcard(one_dict)
            flashcards.append(one_flashcard)
            local_repo.create_flashcard(one_flashcard)

        return local_repo, flashcards

    @staticmethod
    def create_google_repository_with_flashcards(
        *product_data: dict,
    ) -> tuple[google_flashcard_repository.GoogleFlashcardRepository, list[Flashcard]]:
        google_repo = google_flashcard_repository.GoogleFlashcardRepository(
            web_scraper=FakeWebScraper(),
        )

        flashcards: list[Flashcard] = []

        for one_dict in product_data:
            one_product = ServiceClass.get_default_flashcard(one_dict)
            flashcards.append(one_product)

        return google_repo, flashcards
