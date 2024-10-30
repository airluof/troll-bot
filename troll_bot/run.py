import logging
import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Обработчик команды /start
async def start(update, context):
    await update.message.reply_text("Привет! Я бот. Как я могу помочь вам?")

# Обработчик текстовых сообщений
async def echo(update, context):
    log.info(f"Received message: {update.message.text}")  # Логирование сообщения
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

def get_update_handler():
    return MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

def get_start_handler():
    return CommandHandler("start", start)

async def run_bot_service():
    token = os.environ['BOT_TOKEN']  # Получаем токен из переменной окружения
    application = ApplicationBuilder().token(token).build()

    # Добавляем обработчики
    application.add_handler(get_start_handler())  # Обработчик команды /start
    application.add_handler(get_update_handler())  # Обработчик текстовых сообщений

    log.info("Handlers added. Starting bot in polling mode...")
    
    await application.run_polling(poll_interval=0.1)

if __name__ == "__main__":
    asyncio.run(run_bot_service())  # Запускаем функцию
