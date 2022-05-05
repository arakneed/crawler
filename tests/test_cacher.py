import pytest

from arakneed import Config, Cacher


@pytest.fixture
def mem_cacher(logger):
    return Cacher(Config(redis_server=''), logger=logger)


@pytest.fixture
def redis_cacher(logger):
    return Cacher(Config(redis_server='redis://127.0.0.1'), logger=logger)


cacher_matrix = pytest.mark.parametrize('cacher', [
    pytest.lazy_fixture('mem_cacher'),
    pytest.lazy_fixture('redis_cacher')
])


class TestValue:

    @cacher_matrix
    async def test_get_none(self, cacher):
        assert await cacher.get('test_get_none') is None

    @cacher_matrix
    async def test_get_value(self, cacher):
        key = 'test_get_value'
        await cacher.set(key, 1)
        assert await cacher.get(key) == 1

    @cacher_matrix
    async def test_delete(self, cacher):
        key = 'test_delete'
        await cacher.delete(key)
        assert await cacher.get(key) is None
        await cacher.set(key, 1)
        assert await cacher.get(key) == 1
        await cacher.delete(key)
        assert await cacher.get(key) is None


class TestDecr:

    @cacher_matrix
    async def test_decr_none(self, cacher):
        key = 'test_decr_none'
        await cacher.delete(key)
        assert await cacher.decr(key) == -1

    @cacher_matrix
    async def test_decr(self, cacher):
        key = 'test_decr'
        await cacher.set(key, 1)
        assert await cacher.decr(key) == 0
