# Here is the updated code for main.py with explanations for key changes

updated_main_py_content = """
import logging
import os
import asyncio
from telegram.ext import ApplicationBuilder
from troll_bot.webserver import keep_alive  # Импортируем функцию для запуска Flask-сервера

from troll_bot import CERTIFICATE_PATH, BOT_URL
from troll_bot.handler import get_update_handler, get_forward_handler, get_help_handler
from troll_bot.utils import generate_random_string

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

async def run_bot_service():
    token = os.getenv('BOT_TOKEN')  # Получаем токен бота из переменных окружения
    if not token:
        log.error("BOT_TOKEN не найден. Убедитесь, что переменная окружения настроена.")
        return

    application = ApplicationBuilder().token(token).build()

    # Добавляем обработчики
    application.add_handler(get_update_handler())
    application.add_handler(get_forward_handler())
    application.add_handler(get_help_handler())

    if BOT_URL:
        webhook_path = generate_random_string(length=20)
        webhook_uri = '/' + webhook_path
        await set_webhook(application, webhook_uri)  # Установка вебхука
        port = int(os.getenv('PORT', 5000))
        await application.run_webhook(listen='0.0.0.0', port=port, url_path=webhook_uri)
    else:
        await application.run_polling(poll_interval=0.1)

async def set_webhook(application, webhook_uri):
    base_url = BOT_URL
    webhook_url = base_url + webhook_uri
    log.info('Setting URL: %s', webhook_url)

    if CERTIFICATE_PATH:
        with open(CERTIFICATE_PATH, 'rb') as certificate:
            await application.bot.set_webhook(webhook_url, certificate=certificate)
    else:
        await application.bot.set_webhook(webhook_url)

if __name__ == "__main__":
    keep_alive()  # Запускаем Flask-сервер для поддержки вебхука
    asyncio.run(run_bot_service())  # Асинхронно запускаем бота
"""

# Saving updated content to the same file to apply the changes
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(updated_main_py_content)

updated_main_py_content[:1000]  # Display first 1000 characters of the updated file for confirmation
