import importlib
import inspect
import logging
import pkgutil
from typing import Generator, NoReturn

from ticket_bot import exts

logger = logging.getLogger(__name__)


def unqualify(name: str) -> str:
    """Returns an unqualified name if given module/package name"""
    return name.rsplit(".", maxsplit=1)[-1]


def walk_extensions() -> Generator[str, None, None]:
    """Yeilds all extensions name from ticket_bot.exts subpackage"""

    def on_error(name: str) -> NoReturn:
        raise ImportError(name=name)

    for module in pkgutil.walk_packages(
        exts.__path__, f"{exts.__name__}.", onerror=on_error
    ):
        if unqualify(module.name).startswith("_"):
            continue

        imported = importlib.import_module(module.name)
        if not inspect.isfunction(getattr(imported, "setup", None)):
            logger.warn(f"{module.name} doesn't implement setup function")
            continue

        yield module.name
