import asyncio

from .shared import Task, Component


def safe_iter(items):
    try:
        yield from items
    except TypeError:
        yield items


class Scheduler(Component):

    async def run(self, tasks):
        self.queue = asyncio.LifoQueue()
        await self.eat(tasks)

    async def digest(self):
        if self.config.sleep:
            await asyncio.sleep(self.config.sleep)

        return await self.queue.get()

    async def eat(self, tasks, parent=None):
        new_tasks = []
        for task in safe_iter(tasks):
            if await self.is_resolved(task):
                self.logger.warn('duplicate', task)
            else:
                new_tasks.append(task)

        if parent:
            for new_task in new_tasks:
                await self.cacher.set(f"parent:{new_task.key}", parent.key)
            await self.cacher.set(f"children:{parent.key}", len(new_tasks))

        for task in new_tasks:
            self.queue.put_nowait(task)

    async def task_resolved(self, task: Task):
        await self.cacher.set(task.key, 1)

    async def task_succeeded(self, task: Task):
        await self.cacher.set(task.key, 1)
        parent = await self.cacher.get(f"parent:{task.key}")
        if parent:
            await self.cacher.decr(f"children:{parent}")
            if not await self.cacher.get(f"children:{parent}"):
                await self.task_succeeded(Task('node', parent))

    async def task_failed(self, task: Task):
        await self.cacher.set(task.key, 0)

    async def is_resolved(self, task: Task):
        if not self.config.exclusive:
            return False

        resolved = await self.cacher.get(task.key)
        await self.task_resolved(task)
        return resolved

    def task_done(self):
        self.queue.task_done()

    async def all_done(self):
        return await self.queue.join()
