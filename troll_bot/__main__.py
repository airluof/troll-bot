import asyncio
from troll_bot.run import run_bot_service
from webserver import keep_alive  # Импортируем функцию для запуска Flask-сервера

if __name__ == "__main__":
    keep_alive()  # Запускаем Flask-сервер

    try:
        # Проверяем, есть ли уже активный event loop
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # Если нет активного event loop, создаем его
        loop = None

    if loop and loop.is_running():
        # Если цикл уже работает, создаем задачу для run_bot_service
        loop.create_task(run_bot_service())
    else:
        # Если нет активного цикла, создаем и запускаем новый
        asyncio.run(run_bot_service())
