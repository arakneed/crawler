
from dataclasses import dataclass, field


@dataclass
class Config:
    spider: int = 10
    retry: int = 3
    sleep: int = 0
    timeout: int = 3
    tolerant: bool = False
    exclusive: bool = True
    user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'  # noqa

    @property
    def headers(self):
        return {
            'User-Agent': self.user_agent,
        }


@dataclass
class Task:
    type: str
    key: str
    data: dict = field(default_factory=dict, repr=False)


class Component:

    def __init__(self, config: Config, *, cacher=None, logger=None):
        self.config = config
        self.cacher = cacher
        self.logger = logger
