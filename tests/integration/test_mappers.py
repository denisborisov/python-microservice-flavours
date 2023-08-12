"""Integration tests related to mappers."""

from src.adapters import orm
from src.domain import model
from src.routines import mappers


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
        assert not len(resulted_mappers)
