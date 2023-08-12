"""Container with session factory."""

from dependency_injector import containers, providers

from ..services.session_factory import get_default_session_factory


class SessionFactoryContainer(containers.DeclarativeContainer):
    session_factory: providers.Factory = providers.Factory(get_default_session_factory)
