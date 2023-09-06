"""Integration tests related to mappers."""

import sqlalchemy.ext.asyncio

from src.adapters import orm
from src.domain import model
from src.routines import mappers

from .conftest import ServiceClass


class TestMappers:
    def test_imperative_mapping_starts_well(self) -> None:
        expected_result = {
            (model.Article, orm.Article.__table__),
        }

        resulted_mappers = list(mappers.mapper_registry.mappers)

        assert len(resulted_mappers) == 1
        assert (resulted_mappers[0].class_, resulted_mappers[0].local_table) in expected_result

    def test_imperative_mapping_stops_well(self) -> None:
        mappers.stop_mappers()

        resulted_mappers = list(mappers.mapper_registry.mappers)

        assert not resulted_mappers

        mappers.start_mappers()

    async def test_event_attribute_attached_on_load(
        self,
        sqlite_session_factory: sqlalchemy.ext.asyncio.async_sessionmaker,
    ) -> None:
        async with sqlite_session_factory() as session:
            repo, articles = ServiceClass.create_repository_with_articles(
                session,
                {
                    "title": "TITLE",
                    "preview": "PREVIEW",
                    "body": "BODY",
                    "created_by": 1,
                },
            )

            retrieved_article = await repo.retrieve_article_by_id(
                articles[0].article_id,
            )

            assert getattr(retrieved_article, "events", None) is not None
