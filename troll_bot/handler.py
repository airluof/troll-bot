import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from troll_bot.database import save_message
from troll_bot.reply import (get_random_message_word, get_reply_message, should_reply, get_reply_type,
                             reply_text_message, reply_audio_message, reply_gif_message)

log = logging.getLogger(__name__)

def get_update_handler():
    return MessageHandler(filters.TEXT & ~filters.COMMAND, reply_text)  # Изменено на & ~filters.COMMAND

def get_forward_handler():
    return CommandHandler("fwd", forward_message)

def get_help_handler():
    return CommandHandler("help", print_help)

async def reply_text(update, context):
    log.debug('Received: %s', update)

    save_message(update.message)

    # Убедитесь, что сообщение текстовое
    if not update.message.text:
        log.info('Not a text message received.')
        return

    if not should_reply():
        log.info('Should not reply.')
        return

    random_word = get_random_message_word(update.message)
    reply_message = get_reply_message(random_word, update.message.chat.id)
    
    if not reply_message:
        log.info('No reply message found for the random word.')
        return

    reply_type = get_reply_type()

    if reply_type == 'text':
        await reply_text_message(context.bot, update.message.chat.id, reply_message)
    elif reply_type == 'audio':
        await reply_audio_message(context.bot, update.message.chat.id, reply_message)
    elif reply_type == 'gif':
        await reply_gif_message(context.bot, update.message.chat.id, random_word)
    else:
        log.info('Unknown reply type.')

async def forward_message(update, context):
    args = context.args
    if not args:
        log.info('No args passed')
        return

    reply_message = get_reply_message(args[0], update.message.chat.id)
    if not reply_message:
        log.info('No reply message found for the args.')
        return

    await reply_text_message(context.bot, update.message.chat.id, reply_message)

async def print_help(update, context):
    await update.message.reply_text('''/fwd <text> : return some random message with words in <text>''')
