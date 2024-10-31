import asyncio
from troll_bot.run import run_bot_service
from troll_bot.webserver import keep_alive  # Импортируем функцию для запуска Flask-сервера

if __name__ == "__main__":
    keep_alive()  # Запускаем Flask-сервер для поддержки вебхука
    
    # Создаем и запускаем асинхронный event loop для бота
    asyncio.run(run_bot_service())
