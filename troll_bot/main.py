import logging
import sys
import asyncio

from docopt import docopt
from troll_bot.run import run_bot_service

from telegram.ext import ApplicationBuilder  # Импортируем ApplicationBuilder

log = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stderr)

async def main():
    """Troll Bot - Annoy your friends with this Telegram Bot.
    Usage:
      troll-bot [options]
      troll-bot (-h | --help)

    Options:
      --verbose     Show more output
    """
    setup_logging()
    arguments = docopt(main.__doc__)
    setup_console_handler(console_handler, arguments.get('--verbose'))
    
    # Запуск службы бота
    await run_bot_service()  # Измените здесь, чтобы он стал асинхронным

def setup_logging():
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)

def setup_console_handler(handler, verbose):
    if verbose:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)

if __name__ == '__main__':
    asyncio.run(main())  # Запускаем асинхронную функцию main
