import asyncio
from contextlib import asynccontextmanager
from functools import wraps
from urllib import request
from urllib.error import HTTPError

from .exceptions import ResponseTimeoutError, ResponseReadError
from .shared import Task, Component

try:
    import aiohttp
    aiohttp_installed = True
except ImportError:
    aiohttp_installed = False


class Visitor(Component):

    @asynccontextmanager
    async def visit(self, task: Task):
        visit = (
            self.retry(self.aiohttp, self.config.retry, (
                asyncio.exceptions.TimeoutError,
                aiohttp.ClientOSError,
                aiohttp.ServerTimeoutError,
                aiohttp.ServerDisconnectedError,
            ), ResponseTimeoutError)
            if aiohttp_installed else
            self.retry(self.http, self.config.retry, (
                HTTPError,
            ), ResponseTimeoutError)
        )

        async with visit(task.key) as result:
            yield result

    @asynccontextmanager
    async def http(self, url):
        with request.urlopen(url, timeout=self.config.timeout) as connect:
            yield connect

    @asynccontextmanager
    async def aiohttp(self, url):
        try:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:
                async with session.get(url, headers=self.config.headers) as result:
                    yield result
        except aiohttp.ClientPayloadError as e:
            raise ResponseReadError(e) from e

    def retry(self, f, chances: int, expects=Exception, ForwardedError=RuntimeError):
        @asynccontextmanager
        @wraps(f)
        async def visitor(*args, **kwargs):
            try:
                async with f(*args, **kwargs) as result:
                    yield result
            except expects as e:
                if not chances:
                    raise ForwardedError(e) from e
                else:
                    async with self.retry(f, chances - 1, expects, ForwardedError)(*args, **kwargs) as result:
                        yield result

        return visitor
