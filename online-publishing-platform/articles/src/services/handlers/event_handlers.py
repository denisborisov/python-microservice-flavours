"""Event handlers."""

import typing

from ... import domain
from ...services.unit_of_work import AbstractUnitOfWork


EVENT_HANDLERS: dict[
    type[domain.events.Event],
    list[typing.Callable[[domain.events.Event, AbstractUnitOfWork], typing.Awaitable[None]]],
] = {}
