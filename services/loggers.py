import logging
import logging.config
from singleton.singleton import Singleton


@Singleton
class LoggerService:
    config = None
    logger = None

    def __init__(self, config=None):
        if not self.logger:
            self.logger = logging
        if self.config or (config and not self.config):
            current_config = self.config if self.config else config
            self.logger.config.dictConfig(current_config)

    def debug(self, message, exc_info=False):
        self.logger.debug(message, exc_info=exc_info)

    def info(self, message, exc_info=False):
        self.logger.info(message, exc_info=exc_info)

    def warning(self, message, exc_info=False):
        self.logger.warning(message, exc_info=exc_info)

    def error(self, message, exc_info=False):
        self.logger.error(message, exc_info=exc_info)

    def log(self, **kwargs):
        for k in kwargs:
            if k in ['info', 'error', 'debug', 'warning']:
                getattr(self, k)(kwargs[k])
