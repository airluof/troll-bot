import logging
import os
import asyncio
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from troll_bot import CERTIFICATE_PATH, BOT_URL
from troll_bot.handler import get_update_handler, get_forward_handler, get_help_handler
from troll_bot.utils import generate_random_string

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Создаем Flask приложение
app = Flask(__name__)

async def run_bot_service():
    token = os.environ['BOT_TOKEN']  # Получаем токен из переменной окружения
    application = ApplicationBuilder().token(token).build()

    # Добавляем обработчики
    application.add_handler(get_update_handler())
    application.add_handler(get_forward_handler())
    application.add_handler(get_help_handler())

    if BOT_URL:
        webhook_path = generate_random_string(length=20)
        webhook_uri = '/' + webhook_path
        await set_webhook(application, webhook_uri)
        
        # Используем PORT из переменной окружения
        port = int(os.environ.get('PORT', 5000))
        await application.run_webhook(listen='0.0.0.0', port=port, path=webhook_uri)
    else:
        await application.run_polling(poll_interval=0.1)

async def set_webhook(application, webhook_uri):
    base_url = BOT_URL
    webhook_url = base_url + webhook_uri
    log.info('Setting URL: %s', webhook_url)

    if CERTIFICATE_PATH:
        with open(CERTIFICATE_PATH, 'rb') as certificate:
            await application.bot.setWebhook(webhook_url, certificate)
    else:
        await application.bot.setWebhook(webhook_url)

@app.route('/')
def index():
    return 'Bot is running!'

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    # Запуск бота в отдельном потоке
    loop.create_task(run_bot_service())
    
    # Запускаем Flask приложение через Uvicorn
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
