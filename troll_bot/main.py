import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

async def start_handler(update, context):
    await update.message.reply_text('Привет! Я бот. Чем могу помочь?')

async def message_handler(update, context):
    # Обработчик сообщений
    await update.message.reply_text(f'Вы сказали: {update.message.text}')

async def main():
    # Создаем приложение бота
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    # Добавляем обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Инициализируем приложение
    await application.initialize()
    await application.start()
    await application.updater.start_polling(poll_interval=0.1)

if __name__ == "__main__":
    asyncio.run(main())
