
from .shared import Config
from .logger import Logger


class Cacher:

    def __init__(self, config: Config, *, logger: Logger = None):
        self.config = config
        self.logger = logger
        self.store = {}

    def _prefix_key(self, key):
        return f"arakneed:{key}"

    async def get(self, key):
        key = self._prefix_key(key)
        return self.store.get(key)

    async def set(self, key, value):
        key = self._prefix_key(key)
        self.store[key] = value
        return value

    async def decr(self, key):
        key = self._prefix_key(key)
        value = self.store.get(key)
        if not isinstance(value, int):
            value = 0
        self.store[key] = value - 1
        return self.store[key]
