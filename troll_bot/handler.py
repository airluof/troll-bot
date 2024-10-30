import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from troll_bot.database import save_message
from troll_bot.reply import (get_random_message_word, get_reply_message, should_reply, get_reply_type,
                             reply_text_message, reply_audio_message, reply_gif_message)

log = logging.getLogger(__name__)

def get_update_handler():
    return MessageHandler(filters.TEXT, reply_text)

def get_forward_handler():
    return CommandHandler("fwd", forward_message)

def get_help_handler():
    return CommandHandler("help", print_help)

async def reply_text(update, context):
    log.debug('Received update: %s', update)  # Логируем полученное сообщение

    save_message(update.message)  # Сохраняем сообщение в базу данных

    # Проверяем, есть ли у сообщения текст
    if not hasattr(update.message, 'text'):
        log.info('Not a text message received.')
        return

    # Проверяем, следует ли боту отвечать
    if not should_reply():
        log.info('Decided not to reply.')
        return

    # Получаем случайное слово из сообщения
    random_word = get_random_message_word(update.message)
    # Получаем сообщение для ответа на основе случайного слова и ID чата
    reply_message = get_reply_message(random_word, update.message.chat.id)
    if not reply_message:
        log.info('No reply message found for random word: %s', random_word)
        return

    # Получаем тип ответа (текст, аудио, GIF)
    reply_type = get_reply_type()
    log.debug('Reply type determined: %s', reply_type)

    # Отправляем ответ в зависимости от типа
    if reply_type == 'text':
        await reply_text_message(context.bot, update.message.chat.id, reply_message)
    elif reply_type == 'audio':
        await reply_audio_message(context.bot, update.message.chat.id, reply_message)
    elif reply_type == 'gif':
        await reply_gif_message(context.bot, update.message.chat.id, random_word)

async def forward_message(update, context):
    args = context.args
    if not args:
        log.info('No arguments passed to forward command.')
        return

    reply_message = get_reply_message(args[0], update.message.chat.id)
    if not reply_message:
        log.info('No reply message found for argument: %s', args[0])
        return

    await reply_text_message(context.bot, update.message.chat.id, reply_message)

async def print_help(update, context):
    await update.message.reply_text('''/fwd <text> : return some random message with words in <text>''')

# Регистрация обработчиков
def register_handlers(application):
    application.add_handler(get_update_handler())
    application.add_handler(get_forward_handler())
    application.add_handler(get_help_handler())
