import logging
import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from troll_bot import CERTIFICATE_PATH, BOT_URL
from troll_bot.handler import get_update_handler, get_forward_handler, get_help_handler
from troll_bot.utils import generate_random_string

log = logging.getLogger(__name__)

async def run_bot_service():
    token = os.environ['BOT_TOKEN']
    application = ApplicationBuilder().token(token).build()

    # Добавляем обработчики
    application.add_handler(get_update_handler())
    application.add_handler(get_forward_handler())
    application.add_handler(get_help_handler())

    if BOT_URL:
        webhook_path = generate_random_string(length=20)
        webhook_uri = '/' + webhook_path
        await set_webhook(application, webhook_uri)  # Обратите внимание на await
        await application.run_webhook(listen='0.0.0.0', port=5000, path=webhook_uri)
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
