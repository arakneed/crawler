import asyncio
import aiohttp
from pathlib import Path
import re

from arakneed import Crawler, Task, ResponseTimeoutError


async def resolver(task: Task, response: aiohttp.ClientResponse):

    if task.type == 'page':
        r = await response.text()

        return [
            Task('image', group[1])
            for group in re.compile(r'<img.+?src=\"(.+?)\".+?>').finditer(r)
            if group[1].endswith('.jpg') or group[1].endswith('.png') or group[1].endswith('.svg')
        ]

    if task.type == 'image':
        image_path = Path('~/Downloads/gh-images', task.key.split('/')[-1]).expanduser()
        if not image_path.parent.is_dir():
            image_path.parent.mkdir()
        image_path.touch()
        try:
            image_path.write_bytes(await response.content.read())
        except asyncio.exceptions.TimeoutError as e:
            raise ResponseTimeoutError(e) from e


asyncio.run(Crawler().run(Task('page', 'https://github.com'), resolver))
