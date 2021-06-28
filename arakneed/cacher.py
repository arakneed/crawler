import asyncio
from contextlib import asynccontextmanager
import json

from .shared import Config
from .logger import Logger

try:
    import aioredis
    aioredis_installed = True
except ImportError:
    aioredis_installed = False


class CacherBase:

    async def _get_connection(self):
        raise NotImplementedError

    def _prefix_key(self, key):
        return f"arakneed:{key}"

    def _dump_value(self, value):
        return json.dumps(value)

    def _load_value(self, value):
        return json.loads(value)

    async def get(self, key, default=None):
        async with self._get_connection() as conn:
            key = self._prefix_key(key)
            value = await conn.get(key)
            return default if value is None else json.loads(value)

    async def set(self, key, value, **kw):
        async with self._get_connection() as conn:
            key = self._prefix_key(key)
            value = self._dump_value(value)
            return await conn.set(key, value, **kw)

    async def delete(self, key):
        async with self._get_connection() as conn:
            key = self._prefix_key(key)
            return await conn.delete(key)

    async def decr(self, key):
        async with self._get_connection() as conn:
            key = self._prefix_key(key)
            return await conn.decr(key)


class CacherMemConnector:

    def __init__(self):
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, **kw):
        self.store[key] = value
        return value

    async def delete(self, key):
        self.store[key] = None
        return None

    async def decr(self, key):
        value = self.store.get(key)
        if not isinstance(value, int):
            if value is None:
                value = 0
            else:
                try:
                    value = int(value)
                except ValueError:
                    value = 0
        self.store[key] = value - 1
        return self.store[key]


class Cacher(CacherBase):

    def __init__(self, config: Config, *, logger: Logger = None):
        self.config = config
        self.logger = logger
        self.mem_connector = None
        self.redis_enabled = False

        self.try_redis()

    @asynccontextmanager
    async def _get_connection(self):
        if self.redis_enabled:
            yield aioredis.from_url(self.config.redis_server, decode_responses=True)
        else:
            yield self._get_mem_connection()

    def _get_mem_connection(self):
        if not self.mem_connector:
            self.mem_connector = CacherMemConnector()

        return self.mem_connector

    def try_redis(self):
        async def try_connect():
            redis = aioredis.from_url(self.config.redis_server, decode_responses=True)
            connection = await redis.connection_pool.get_connection("_")
            await connection.connect()
            await connection.disconnect()

        if self.config.redis_server:
            if aioredis_installed:
                try:
                    asyncio.get_event_loop().run_until_complete(try_connect())
                    self.redis_enabled = True
                except Exception:
                    self.logger.error('Exception', 'invalid redis server', str(self.config.redis_server))
                    raise
            else:
                self.logger.error('Exception', 'aioredis is not installed')
