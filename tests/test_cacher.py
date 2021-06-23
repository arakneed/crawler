class TestGet:

    async def test_get_none(self, cacher):
        assert await cacher.get('test_get_none') is None

    async def test_get_value(self, cacher):
        key = 'test_get_value'
        await cacher.set(key, 1)
        assert await cacher.get(key) == 1


class TestDecr:

    async def test_decr_none(self, cacher):
        assert await cacher.decr('test_decr_none') == -1

    async def test_decr(self, cacher):
        key = 'test_decr'
        await cacher.set(key, 1)
        assert await cacher.decr(key) == 0
