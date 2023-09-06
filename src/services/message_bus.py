"""Message bus."""

import asyncio
import contextlib
import typing

import dependency_injector.wiring

from ..containers.unit_of_work import SqlAlchemyUnitOfWorkContainer
from ..domain.commands import Command
from ..domain.events import Event
from ..domain.exceptions import CommandHandlingError
from ..services import handlers
from ..services.unit_of_work import AbstractUnitOfWork


class MessageBus:
    @dependency_injector.wiring.inject
    def __init__(
        self,
        uow: AbstractUnitOfWork = dependency_injector.wiring.Provide[
            SqlAlchemyUnitOfWorkContainer.sql_alchemy_unit_of_work
        ],
    ) -> None:
        self.uow = uow
        self._event_queue: asyncio.Queue[Event] = asyncio.Queue()
        self._command_handlers = handlers.command_handlers.COMMAND_HANDLERS
        self._event_handlers = handlers.event_handlers.EVENT_HANDLERS
        self._pending_handle_event_tasks: set[asyncio.Task] = set()

    def start_process_events(self) -> None:
        self._process_events_task = asyncio.create_task(self._process_events())

    async def _process_events(self) -> None:
        while event := await self._event_queue.get():
            self._pending_handle_event_tasks = {
                task for task in self._pending_handle_event_tasks if not task.done()
            }
            self._pending_handle_event_tasks.add(asyncio.create_task(self._handle_event(event)))
            self._event_queue.task_done()

    async def stop_process_events(self) -> None:
        while self._pending_handle_event_tasks or self._event_queue.qsize():
            self._pending_handle_event_tasks = {
                task for task in self._pending_handle_event_tasks if not task.done()
            }
            await asyncio.gather(self._event_queue.join(), *self._pending_handle_event_tasks)

        self._process_events_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._process_events_task

    async def handle(self, command: Command) -> typing.Any:
        return await self._handle_command(command)

    async def _handle_command(self, command: Command) -> typing.Any:
        try:
            handler = self._command_handlers[type(command)]
        except KeyError:
            raise CommandHandlingError(
                f"Cannot find a command handler for {type(command)}",
            ) from KeyError

        result = await handler(command, self.uow)
        for one_event in self.uow.collect_new_events():
            await self._event_queue.put(one_event)
        return result

    async def _handle_event(self, event: Event) -> None:
        for handler in self._event_handlers[type(event)]:
            await handler(event, self.uow)
            for one_event in self.uow.collect_new_events():
                await self._event_queue.put(one_event)
