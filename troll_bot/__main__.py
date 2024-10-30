import asyncio
from troll_bot.main import main

if __name__ == "__main__":
    try:
        asyncio.run(main())  # Попробуем запустить с помощью asyncio.run()
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(main())  # Запускаем асинхронную задачу, если цикл уже запущен
        else:
            raise
