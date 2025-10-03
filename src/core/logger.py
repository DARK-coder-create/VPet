# logger.py с дополнениями
from loguru import logger as loguru_logger
import sys
import logging
from pathlib import Path


class LoggerSetup:
    def __init__(self, log_dir="logs", level="DEBUG", format_string=None):
        self.log_dir = Path(log_dir)
        self.level = level
        self.format_string = format_string or self._default_format()
        self.handlers = []
        self._setup_done = False

    @staticmethod
    def _default_format():
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )

    def add_console_handler(self, level=None, colorize=True):
        handler = {
            "sink": sys.stderr,
            "format": self.format_string,
            "level": level or self.level,
            "colorize": colorize,
            "backtrace": True,
            "diagnose": True
        }
        self.handlers.append(handler)

    def add_file_handler(self, filename, level=None, rotation="10 MB", retention="30 days"):
        handler = {
            "sink": self.log_dir / filename,
            "format": self.format_string,
            "level": level or self.level,
            "rotation": rotation,
            "retention": retention,
            "compression": "zip",
            "enqueue": True,
            "backtrace": True,
            "diagnose": True
        }
        self.handlers.append(handler)

    def _setup_standard_logging_intercept(self):
        """Перехватывает стандартный logging и перенаправляет в loguru"""

        class InterceptHandler(logging.Handler):
            def emit(self, record):
                try:
                    level = loguru_logger.level(record.levelname).name
                except ValueError:
                    level = record.levelno

                frame, depth = logging.currentframe(), 6
                while frame and frame.f_code.co_filename == logging.__file__:
                    frame = frame.f_back
                    depth += 1

                loguru_logger.opt(depth=depth, exception=record.exc_info).log(
                    level, record.getMessage()
                )

        handler = InterceptHandler()
        handler.setLevel(logging.DEBUG)

        logging.basicConfig(handlers=[handler], level=logging.DEBUG, force=True)

        # Для lupa и других библиотек
        for lib_name in ['lupa']:
            lib_logger = logging.getLogger(lib_name)
            lib_logger.handlers = [handler]
            lib_logger.propagate = False
            lib_logger.setLevel(logging.DEBUG)

    def setup(self):
        if self._setup_done:
            return loguru_logger

        self.log_dir.mkdir(exist_ok=True)
        loguru_logger.remove()

        if not self.handlers:
            self._add_default_handlers()

        for handler in self.handlers:
            loguru_logger.add(**handler)

        # Перенаправляем стандартный logging
        self._setup_standard_logging_intercept()

        self._setup_done = True
        return loguru_logger

    def _add_default_handlers(self):
        if sys.stderr:
            self.add_console_handler()
        self.add_file_handler("app_{time}.log")
        self.add_file_handler("errors_{time}.log", level="ERROR", rotation="5 MB", retention="60 days")


# Глобальный логгер
logger = LoggerSetup().setup()