"""Unit tests related to message bus."""

import time

import pytest

from src import routines
from src.domain.commands import Command
from src.domain.exceptions import CommandHandlingError
from src.services.message_bus import MessageBus

from . import conftest


class ServiceClass:
    class NonExistentCommand(Command):
        pass

    @staticmethod
    async def start_and_stop_processing_events(fake_bus: MessageBus) -> tuple[float, float]:
        start = time.time()
        fake_bus.start_process_events()
        await fake_bus.stop_process_events()
        stop = time.time()
        return (start, stop)

    @staticmethod
    def one_event_has_been_processed(capsys: pytest.CaptureFixture) -> bool:
        std_out: str = capsys.readouterr().out
        return std_out == "."


class TestMessageBus:
    async def test_can_handle_command(self, fake_bus: MessageBus) -> None:
        await fake_bus.handle(
            conftest.CreateArticleWithTwoEvents(
                conftest.SayHello("spam"),
                conftest.SendTwoEmails("eggs"),
            ),
        )

        articles = await fake_bus.uow.article_repository.retrieve_all_articles()

        assert len(articles) == 1
        assert fake_bus._event_queue.qsize() == 2  # noqa: SLF001, PLR2004

    async def test_cannot_handle_nonexistent_command(self, fake_bus: MessageBus) -> None:
        command = ServiceClass.NonExistentCommand()

        with pytest.raises(CommandHandlingError) as exc_info:
            await fake_bus.handle(command)

        assert exc_info.value.args[0] == f"Cannot find a command handler for {type(command)}"

    async def test_can_handle_events(
        self,
        fake_bus: MessageBus,
        capsys: pytest.CaptureFixture,
    ) -> None:
        await conftest.handle(
            fake_bus,
            conftest.CreateArticleWithTwoEvents(
                conftest.SayHello("spam"),
                conftest.SendTwoEmails("eggs"),
            ),
        )

        assert not fake_bus._event_queue.qsize()  # noqa: SLF001
        assert capsys.readouterr().out == "spam\neggs\neggs\n"


class TestEventsProcessingCycle:
    async def test_can_start_and_stop_process_events_in_bus(self, fake_bus: MessageBus) -> None:
        routines.message_bus.start_process_events_in_bus(bus=fake_bus)
        assert not fake_bus._process_events_task.done()  # noqa: SLF001

        await routines.message_bus.stop_process_events_in_bus(bus=fake_bus)
        assert fake_bus._process_events_task.done()  # noqa: SLF001

    async def test_queued_events_are_finished_before_stop_processing_events(
        self,
        fake_bus: MessageBus,
        capsys: pytest.CaptureFixture,
    ) -> None:
        await fake_bus._event_queue.put(conftest.SleepEvent(1))  # noqa: SLF001

        await ServiceClass.start_and_stop_processing_events(fake_bus)

        assert ServiceClass.one_event_has_been_processed(capsys)

    async def test_queued_events_are_processed_asynchronously(self, fake_bus: MessageBus) -> None:
        for one_event in [conftest.SleepEvent(1) for _ in range(10)]:
            await fake_bus._event_queue.put(one_event)  # noqa: SLF001

        start, stop = await ServiceClass.start_and_stop_processing_events(fake_bus)

        assert stop - start < 2  # noqa: PLR2004
