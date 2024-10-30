import asyncio
from troll_bot.main import main

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Если цикл событий уже запущен, используем его для выполнения main
            loop.create_task(main())
        else:
            # Если цикл не запущен, запускаем его
            asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")
