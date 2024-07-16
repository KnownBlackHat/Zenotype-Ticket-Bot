import asyncio

from ticket_bot import TicketBot, log


async def main():
    log.setup_logging()
    bot = TicketBot()


asyncio.run(main())
