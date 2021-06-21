import asyncio
from contextlib import asynccontextmanager
from functools import wraps

import aiohttp
from .exceptions import ResponseTimeoutError, ResponseReadError
from .shared import Task, Component


class Visitor(Component):

    @asynccontextmanager
    async def visit(self, task: Task):
        visit = self.retry(self.aiohttp, self.config.retry, (
            asyncio.exceptions.TimeoutError,
            aiohttp.ClientOSError,
            aiohttp.ServerTimeoutError,
            aiohttp.ServerDisconnectedError,
        ), ResponseTimeoutError)

        async with visit(task.key) as result:
            yield result

    @asynccontextmanager
    async def aiohttp(self, url):
        try:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
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
