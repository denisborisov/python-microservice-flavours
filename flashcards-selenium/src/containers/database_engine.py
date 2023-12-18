"""Container with database engine."""

from dependency_injector import containers, providers

from ..services.database_engine import get_database_engine


class DatabaseEngineContainer(containers.DeclarativeContainer):
    database_engine: providers.Factory = providers.Factory(get_database_engine)
