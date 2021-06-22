from .shared import Component
from .exceptions import CrawlerError
from .visitor import Visitor
from .scheduler import Scheduler


class Spider(Component):

    def install(self, *, scheduler: Scheduler, visitor: Visitor):
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
