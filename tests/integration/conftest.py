"""Fixtures related to integration tests."""

import pytest
import typing

from src.routines import mappers


@pytest.fixture(scope="module", autouse=True)
def _use_mappers() -> typing.Generator:
    mappers.start_mappers()
    yield
    mappers.stop_mappers()
