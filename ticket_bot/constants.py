import os


class Database:
    db_name = "ticket_bot.db"
    uri = f"sqlite+aiosqlite:///{db_name}"


class Client:
    name = "Ticket Bot"
    token = os.getenv("BOT_TOKEN", "")
    log_file_name = "logs/ticket_bot.log"
    prefix = "~"
