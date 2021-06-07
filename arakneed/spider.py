from .shared import Config
from .exceptions import CrawlerError
from .visitor import Visitor
from .logger import Logger
from .scheduler import Scheduler


class Spider:

    def __init__(self, config: Config, scheduler: Scheduler, visitor: Visitor, logger: Logger):
        self.config = config
        self.logger = logger
        self.scheduler = scheduler
        self.visitor = visitor

    async def run(self, resolver):
        while True:
            try:
                task = await self.scheduler.digest()
                self.logger.info('Resolving', task)
                async with self.visitor.visit(task) as result:
                    tasks = await resolver(task, result)
                    if tasks:
                        await self.scheduler.eat(tasks, task)
                    else:
                        await self.scheduler.task_succeeded(task)
            except CrawlerError as e:
                self.logger.error('Failure', repr(e.raw_error), task)
                await self.scheduler.task_failed(task)
            except Exception as e:
                self.logger.error('Exception', e)
                if not self.config.tolerant:
                    raise
            finally:
                self.scheduler.task_done()
