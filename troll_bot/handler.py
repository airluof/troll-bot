async def reply_text(update, context):
    log.debug('Received update: %s', update)
    save_message(update.message)

    if not hasattr(update.message, 'text'):
        log.info('Not a text message received.')
        return

    if not should_reply():
        log.info('Decided not to reply.')
        return

    random_word = get_random_message_word(update.message)
    reply_message = get_reply_message(random_word, update.message.chat.id)
    if not reply_message:
        log.info('No reply message found for random word: %s', random_word)
        return

    reply_type = get_reply_type()
    log.debug('Reply type determined: %s', reply_type)

    if reply_type == 'text':
        await reply_text_message(context.bot, update.message.chat.id, reply_message)
    elif reply_type == 'audio':
        await reply_audio_message(context.bot, update.message.chat.id, reply_message)
    elif reply_type == 'gif':
        await reply_gif_message(context.bot, update.message.chat.id, random_word)
