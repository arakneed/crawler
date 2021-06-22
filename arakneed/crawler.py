import asyncio

from .shared import Config
from .logger import Logger
from .cacher import Cacher
from .visitor import Visitor
from .spider import Spider
from .scheduler import Scheduler


class Crawler:

    Logger = Logger
    Cacher = Cacher
    Scheduler = Scheduler
    Visitor = Visitor
    Spider = Spider

    def __init__(self, config: Config = Config()):
        self.config = config
        self.logger = self.Logger(config)
        self.cacher = self.Cacher(config, logger=self.logger)
        self.scheduler = self.Scheduler(config, cacher=self.cacher, logger=self.logger)
        self.visitor = self.Visitor(config, cacher=self.cacher, logger=self.logger)

    async def run(self, tasks, resolver):
        await self.scheduler.run(tasks)

        aio_tasks = []
        for _ in range(self.config.spider):
            spider = self.Spider(self.config, cacher=self.cacher, logger=self.logger)
            spider.install(scheduler=self.scheduler, visitor=self.visitor)
            aio_tasks.append(asyncio.create_task(spider.run(resolver)))

        await self.scheduler.all_done()

        for task in aio_tasks:
            task.cancel()

        self.logger.info('DONE')

        return await asyncio.gather(*aio_tasks, return_exceptions=True)
