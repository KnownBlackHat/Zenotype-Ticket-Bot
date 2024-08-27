import os


class Client:
    name = "Ticket Bot"
    token = os.getenv("BOT_TOKEN", "")
    log_file_name = "logs/ticket_bot.log"
    prefix = "~"
    ipc_url = "http://localhost:8080"


class Colours:
    white = 0xFFFFFF
    blue = 0x0279FD
    bright_green = 0x01D277
    dark_green = 0x1F8B4C
    orange = 0xE67E22
    pink = 0xCF84E0
    purple = 0xB734EB
    green = 0x68C290
    orange = 0xF9CB54
    red = 0xCD6D6D
    yellow = 0xF9F586
    python_blue = 0x4B8BBE
    python_yellow = 0xFFD43B
    grass_green = 0x66FF00
    gold = 0xE6C200
