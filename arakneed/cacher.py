
from .shared import Config
from .logger import Logger


class Cacher:

    def __init__(self, config: Config, *, logger: Logger = None):
        self.config = config
        self.logger = logger
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value):
        self.store[key] = value
        return value

    async def decr(self, key):
        value = self.store.get(key)
        if not isinstance(value, int):
            value = 0
        self.store[key] = value - 1
        return self.store[key]
