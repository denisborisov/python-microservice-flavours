"""Routines related to database engine."""

import dependency_injector.wiring
from sqlalchemy.ext.asyncio import AsyncEngine

from ..containers.database_engine import DatabaseEngineContainer


@dependency_injector.wiring.inject
async def dispose_database_engine(
    engine: AsyncEngine = dependency_injector.wiring.Provide[
        DatabaseEngineContainer.database_engine
    ],
) -> None:
    await engine.dispose()
