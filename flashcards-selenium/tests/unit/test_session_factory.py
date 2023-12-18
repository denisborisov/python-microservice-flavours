"""Integration tests related to session factory."""

import sqlalchemy.ext.asyncio

from src.services.session_factory import get_default_session_factory


class TestSessionFactory:
    def test_session_factory_has_needed_attributes(
        self,
        in_memory_sqlite_db: sqlalchemy.ext.asyncio.AsyncEngine,
    ) -> None:
        session_factory: sqlalchemy.ext.asyncio.async_sessionmaker = get_default_session_factory(
            engine=in_memory_sqlite_db,
        )

        assert session_factory.kw["bind"] == in_memory_sqlite_db
        assert not session_factory.kw["autocommit"]
        assert not session_factory.kw["autoflush"]
        assert not session_factory.kw["expire_on_commit"]
