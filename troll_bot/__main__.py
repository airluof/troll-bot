import logging
import asyncio
from troll_bot.run import run_bot_service

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Запуск асинхронной функции в текущем цикле событий
    try:
        asyncio.run(run_bot_service())
    except RuntimeError as e:
        if str(e) == "This event loop is already running":
            loop = asyncio.get_event_loop()
            loop.create_task(run_bot_service())  # Запускаем функцию в уже запущенном цикле
        else:
            raise e
