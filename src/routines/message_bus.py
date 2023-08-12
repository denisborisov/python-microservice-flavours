"""Routines related to message bus."""

import dependency_injector.wiring

from ..containers.message_bus import MessageBusContainer
from ..services.message_bus import MessageBus


@dependency_injector.wiring.inject
def start_process_events_in_bus(
    bus: MessageBus = dependency_injector.wiring.Provide[MessageBusContainer.message_bus],
) -> None:
    bus.start_process_events()


async def stop_process_events_in_bus(
    bus: MessageBus = dependency_injector.wiring.Provide[MessageBusContainer.message_bus],
) -> None:
    await bus.stop_process_events()
