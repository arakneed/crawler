
from functools import wraps
import logging
import platform

from .shared import Config


class HostnameFilter(logging.Filter):
    hostname = platform.node()

    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True


class Logger:

    def __init__(self, config: Config):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(f"{__name__}.log")
        file_handler.setLevel(logging.ERROR)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        hostname_filter = HostnameFilter()
        file_handler.addFilter(hostname_filter)
        console_handler.addFilter(hostname_filter)

        formatter = logging.Formatter(
            '%(asctime)s %(hostname)s %(name)s[%(process)d]: %(levelname)s - %(message)s',
            datefmt='%b  %d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        self.logger = logger

    def __proxy(name):
        def decorator(fn):
            @wraps(fn)
            def decorated(self, *args, **kwargs):
                getattr(self.logger, name)(' '.join(str(arg) for arg in args), **kwargs)
            return decorated
        return decorator

    @__proxy('debug')
    def debug(self):
        pass

    @__proxy('info')
    def info(self):
        pass

    @__proxy('warn')
    def warn(self):
        pass

    @__proxy('warning')
    def warning(self):
        pass

    @__proxy('error')
    def error(self):
        pass

    @__proxy('fatal')
    def fatal(self):
        pass
