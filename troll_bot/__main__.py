import asyncio
from troll_bot.run import run_bot_service
from webserver import keep_alive  # Запускаем Flask-сервер

if __name__ == "__main__":
    keep_alive()  # Запускаем Flask-сервер
    
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # Если цикла нет, он будет запущен
        loop = None

    if loop and loop.is_running():
        # Если цикл уже работает, создаем задачу для run_bot_service
        loop.create_task(run_bot_service())
    else:
        # Если цикл еще не запущен, используем asyncio.run()
        asyncio.run(run_bot_service())
