
from .shared import Task


class CrawlerError(RuntimeError):
    def __init__(self, raw_error, task=None):
        self.raw_error = raw_error
        self.task = task or Task('', '')

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"CrawlerError: {self.raw_error} - {self.task.key}"


class ResponseReadError(CrawlerError):
    pass


class DuplicatedTaskError(CrawlerError):
    pass


class ResponseTimeoutError(CrawlerError):
    pass
