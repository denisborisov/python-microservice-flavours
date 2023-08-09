"""Session factory."""

import dependency_injector.wiring
import sqlalchemy.ext.asyncio

from ..containers.database_engine import DatabaseEngineContainer


@dependency_injector.wiring.inject
def get_default_session_factory(
    engine: sqlalchemy.ext.asyncio.AsyncEngine = dependency_injector.wiring.Provide[
        DatabaseEngineContainer.database_engine
    ],
) -> sqlalchemy.ext.asyncio.async_sessionmaker:
    return sqlalchemy.ext.asyncio.async_sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
