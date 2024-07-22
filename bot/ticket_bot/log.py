import logging.config
import logging.handlers
from pathlib import Path

import colorama

from ticket_bot.constants import Client


class LogFormatter(logging.Formatter):
    colormap = {
        logging.DEBUG: colorama.Fore.MAGENTA,
        logging.INFO: colorama.Fore.BLUE,
        logging.WARNING: colorama.Fore.YELLOW,
        logging.ERROR: colorama.Fore.RED,
        logging.CRITICAL: colorama.Fore.WHITE,
    }

    def __init__(self, format: str) -> None:
        super().__init__(format)

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = f"{self.colormap.get(record.levelno)}{record.levelname}{colorama.Fore.RESET}"
        return super().format(record)


def setup_logging() -> None:
    root_logger = logging.getLogger()

    log_file = Path(Client.log_file_name)
    log_file.parent.mkdir(exist_ok=True)

    formatter = LogFormatter(
        "[ %(levelname)s | %(name)s | %(module)s | L%(lineno)d ] %(asctime)s: %(message)s"
    )
    file_formatter = logging.Formatter(
        "[ %(levelname)s | %(name)s | %(module)s | %(funcName)s | %(filename)s | L%(lineno)d ] %(asctime)s: %(message)s"
    )

    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        mode="a",
        # File handler rotates log every 5 MB
        maxBytes=5 * (2**20),
        backupCount=10,
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)

    root_logger.setLevel(logging.DEBUG)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("mafic").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("disnake").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("core").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.orm").setLevel(logging.WARNING)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)
    logging.getLogger("streamlink").disabled = True

    root_logger.info("Logger Initialized!")
