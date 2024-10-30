import logging
import asyncio
from troll_bot.run import run_bot_service

async def main():
    await run_bot_service()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        # Проверяем, есть ли уже запущенный цикл событий
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Если цикл событий уже запущен, создаем задачу
            asyncio.ensure_future(main())
        else:
            # Если цикл событий не запущен, запускаем его
            loop.run_until_complete(main())
    except Exception as e:
        logging.error(f"Ошибка при запуске: {e}")
