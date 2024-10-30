import logging
import os
import asyncio
from telegram.ext import ApplicationBuilder
from webserver import keep_alive  # Импортируем функцию для запуска Flask-сервера

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
        webhook_path = generate_random_string(length=20)  # Генерируем случайный путь для вебхука
        webhook_uri = '/' + webhook_path
        await set_webhook(application, webhook_uri)  # Устанавливаем вебхук
        await check_webhook(application)  # Проверка установленного вебхука
        port = int(os.environ.get("PORT", 5000))
        log.info(f"Запуск в режиме вебхука на порту {port} с URL: {BOT_URL}")
        await application.run_webhook(listen='0.0.0.0', port=port, path=webhook_uri)
    else:
        log.info("Запуск в режиме опроса (polling)")
        await application.run_polling(poll_interval=0.1)  # Запускаем бота в режиме опроса

async def set_webhook(application, webhook_uri):
    base_url = BOT_URL
    webhook_url = base_url + webhook_uri
    log.info('Установка вебхука по URL: %s', webhook_url)  # Логируем установку вебхука

    try:
        if CERTIFICATE_PATH:
            with open(CERTIFICATE_PATH, 'rb') as certificate:
                await application.bot.setWebhook(webhook_url, certificate=certificate)  # Устанавливаем вебхука с сертификатом
        else:
            await application.bot.setWebhook(webhook_url)  # Устанавливаем вебхука без сертификата
    except Exception as e:
        log.error(f"Ошибка при установке вебхука: {e}")

async def check_webhook(application):
    webhook_info = await application.bot.getWebhookInfo()
    log.info("Текущая информация о вебхуке: %s", webhook_info)  # Логируем информацию о вебхуке

# Тестовая функция для отправки тестового сообщения
async def test_send_message(application):
    bot = application.bot
    chat_id = <ВАШ_ЧАТ_ID>
    try:
        await bot.sendMessage(chat_id=chat_id, text="Тестовое сообщение")
        log.info("Тестовое сообщение отправлено успешно.")
    except Exception as e:
        log.error(f"Не удалось отправить тестовое сообщение: {e}")

if __name__ == "__main__":
    keep_alive()  # Запускаем Flask-сервер для поддержания активности
    application = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()
    asyncio.run(test_send_message(application))  # Тестовая отправка сообщения
    asyncio.run(run_bot_service())  # Запускаем бота
