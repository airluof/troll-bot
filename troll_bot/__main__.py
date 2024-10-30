import asyncio
from troll_bot.run import run_bot_service
from webserver import keep_alive  # Запуск Flask-сервера

if __name__ == "__main__":
    keep_alive()  # Запускаем Flask-сервер
    asyncio.run(run_bot_service())  # Запускаем бота
