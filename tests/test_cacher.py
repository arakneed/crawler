class TestValue:

    async def test_get_none(self, cacher):
        assert await cacher.get('test_get_none') is None

    async def test_get_value(self, cacher):
        key = 'test_get_value'
        await cacher.set(key, 1)
        assert await cacher.get(key) == 1

    async def test_delete(self, cacher):
        key = 'test_delete'
        await cacher.delete(key)
        assert await cacher.get(key) is None
        await cacher.set(key, 1)
        assert await cacher.get(key) == 1
        await cacher.delete(key)
        assert await cacher.get(key) is None


class TestDecr:

    async def test_decr_none(self, cacher):
        key = 'test_decr_none'
        await cacher.delete(key)
        assert await cacher.decr(key) == -1

    async def test_decr(self, cacher):
        key = 'test_decr'
        await cacher.set(key, 1)
        assert await cacher.decr(key) == 0
