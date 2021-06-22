# Arakneed

A common use targeted concurrent crawler for **any** directed graph. It's designed to be easy to use.

It's an adequate practice to organize your crawler code instead of a spider library or framework.

## Why this since there's scrapy .etc?

Because they are not supposed to crawl my pictures on my laptop but I want to crawl them like a spider.

Arakneed can be used to traverse any directed graph, including a directory on your computer to collect pictures or collecting someone's all Github Gists... And anything looks like directed graph.

Though it can also be used to crawl a website like a tranditional spider.

## How to use?

Any vertex spotted by the spider will be scheduled as a **task**. The only thing you need to do is to define how to handle the tasks.

```python
import asyncio
from pathlib import Path
import re

import aiohttp
from arakneed import Crawler, Task


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
        image_path.write_bytes(await response.content.read())


asyncio.run(Crawler().run(Task('page', 'https://github.com'), resolver))
```

This code downloads all images it founds on Github. I believe it explains what does the business code look like.

## Examples

- Crawl a website
- Collect pictures in a local driver
- Abstract Syntax Tree analyzer

## MISC

- Be careful with circles in the directed graph if you are customizing the scheduler/spider. The framework always checks whether all corresponding vertices are resolved recursively of every vertex to know when could it have a relax :)
- This paradigm is not distributed. Though you can take a glance of it through Redis based vertices resolving check, but the task is locked as soon as it's resolved, you cannot resolve a task on several machines simultaneously.
