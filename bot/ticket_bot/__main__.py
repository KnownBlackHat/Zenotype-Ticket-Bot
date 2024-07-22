import asyncio
import logging
import signal
import sys

import disnake

from ticket_bot import TicketBot, log
from ticket_bot.constants import Client


async def main():
    log.setup_logging()
    logger = logging.getLogger(Client.name)
    bot = TicketBot(intents=disnake.Intents.all(), command_prefix=Client.prefix)
    await bot.init_db()
    try:
        bot.load_bot_extensions()
    except Exception:
        await bot.close()
        logger.error("Error occured while loading extension", exc_info=True)
        raise

    loop = asyncio.get_running_loop()

    future: asyncio.Future = asyncio.ensure_future(bot.start(Client.token), loop=loop)

    loop.add_signal_handler(signal.SIGINT, lambda: future.cancel())
    loop.add_signal_handler(signal.SIGTERM, lambda: future.cancel())

    try:
        await future
    except asyncio.CancelledError:
        logger.warn("Received signal to terminate bot and event loop")
    finally:
        logger.warning("Closing bot")
        if bot.is_closed():
            await bot.close()
        exit()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
