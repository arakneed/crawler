from asyncio import iscoroutinefunction as isasync

import pytest

from arakneed import Config, Cacher, Logger, Visitor


def pytest_collection_modifyitems(items):
    for item in items:
        if isasync(item.function):
            item.add_marker('asyncio')


@pytest.fixture
def config():
    return Config()


@pytest.fixture
def cacher(config):
    return Cacher(config)


@pytest.fixture
def logger(config):
    return Logger(config)


@pytest.fixture
def visitor(config, cacher, logger):
    return Visitor(config, cacher=cacher, logger=logger)
