"""Container with message bus."""

from dependency_injector import containers, providers

from ..services.message_bus import MessageBus


class MessageBusContainer(containers.DeclarativeContainer):
    message_bus: providers.Singleton = providers.Singleton(MessageBus)
