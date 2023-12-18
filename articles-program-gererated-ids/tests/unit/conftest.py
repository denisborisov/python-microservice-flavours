"""Fixtures related to unit tests."""

import asyncio
import uuid
from dataclasses import dataclass

import pytest

from src.adapters.articles_repository import AbstractArticleRepository
from src.domain import model
from src.domain.commands import Command
from src.domain.events import Event
from src.services.message_bus import MessageBus
from src.services.unit_of_work import AbstractUnitOfWork


class FakeArticleRepository(AbstractArticleRepository):
    def __init__(self) -> None:
        self.articles: set[model.Article] = set()
        self.seen: set[model.Article] = set()

    def _create_article(self, article: model.Article) -> None:
        article.article_id = uuid.uuid4()
        self.articles.add(article)

    async def _retrieve_article_by_id(self, article_id: uuid.UUID) -> model.Article | None:
        if filtered_articles := [
            one_article for one_article in self.articles if one_article.article_id == article_id
        ]:
            return filtered_articles[0]
        return None

    async def _retrieve_all_articles(self, created_by: int | None) -> list[model.Article]:
        if created_by:
            return [article for article in self.articles if article.created_by == created_by]
        return list(self.articles)

    async def _delete_article(self, article: model.Article) -> None:
        self.articles.remove(article)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self.article_repository = FakeArticleRepository()
        self.committed = False

    async def _commit(self) -> None:
        self.committed = True

    async def _rollback(self) -> None:
        pass


@dataclass
class CreateArticleWithTwoEvents(Command):
    first_event: Event
    second_event: Event


@dataclass
class SayHello(Event):
    message: str


@dataclass
class SendTwoEmails(Event):
    message: str


@dataclass
class SleepEvent(Event):
    seconds: float


async def say_hello(
    event: SayHello,
    _: AbstractUnitOfWork,
) -> None:
    print(f"{event.message}")  # noqa: T201


async def send_first_email(
    event: SendTwoEmails,
    _: AbstractUnitOfWork,
) -> None:
    print(f"{event.message}")  # noqa: T201


async def send_second_email(
    event: SendTwoEmails,
    _: AbstractUnitOfWork,
) -> None:
    print(f"{event.message}")  # noqa: T201


async def sleep_for(
    event: SleepEvent,
    _: AbstractUnitOfWork,
) -> None:
    print(".", end="")  # noqa: T201
    await asyncio.sleep(event.seconds)


event_handlers = {
    SayHello: [say_hello],
    SendTwoEmails: [send_first_email, send_second_email],
    SleepEvent: [sleep_for],
}


async def create_article_with_two_events(
    cmd: CreateArticleWithTwoEvents,
    uow: AbstractUnitOfWork,
) -> None:
    article = model.Article("Title", "Preview", "Body", created_by=1)
    article.events = [cmd.first_event, cmd.second_event]
    uow.article_repository.create_article(article)


command_handlers = {
    CreateArticleWithTwoEvents: create_article_with_two_events,
}


@pytest.fixture()
def fake_uow() -> FakeUnitOfWork:
    return FakeUnitOfWork()


@pytest.fixture()
def fake_bus(fake_uow: AbstractUnitOfWork) -> MessageBus:
    bus = MessageBus(uow=fake_uow)
    bus._command_handlers = command_handlers  # type: ignore[assignment]  # noqa: SLF001
    bus._event_handlers = event_handlers  # type: ignore[assignment]  # noqa: SLF001
    return bus


async def handle(fake_bus: MessageBus, command: Command) -> None:
    fake_bus.start_process_events()
    await fake_bus.handle(command)
    await fake_bus.stop_process_events()
