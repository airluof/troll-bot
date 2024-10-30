import logging
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

async def reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.info('Received update: %s', update)
    # Основная логика обработки текста
    await update.message.reply_text("Привет! Я бот.")

def get_update_handler():
    return CommandHandler("update", reply_text)  # Обработчик для команды /update

def get_forward_handler():
    return MessageHandler(Filters.forwarded, reply_text)  # Обработчик для пересланных сообщений

def get_help_handler():
    return CommandHandler("help", reply_text)  # Обработчик для команды /help
