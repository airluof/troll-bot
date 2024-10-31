import os
import logging
import asyncpg
from datetime import datetime

# Установка уровня логирования
logging.basicConfig(level=logging.DEBUG)

# Подключение к PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    logging.error("DATABASE_URL is not set.")
else:
    logging.info("DATABASE_URL is set: %s", DATABASE_URL)

async def connect_to_db():
    try:
        # Подключение к базе данных
        conn = await asyncpg.connect(DATABASE_URL)
        logging.info("Successfully connected to PostgreSQL.")
        return conn
    except Exception as e:
        logging.error("Failed to connect to PostgreSQL: %s", e)
        return None

async def save_message(message):
    conn = await connect_to_db()
    if conn is None:
        logging.error("Database connection is not established. Message cannot be saved.")
        return

    # Проверка наличия необходимых атрибутов в сообщении
    if not hasattr(message, 'chat') or not hasattr(message, 'from_user') or not hasattr(message, 'text'):
        logging.warning('Message is missing required attributes.')
        return

    message_data = {
        'chat_id': message.chat.id,
        'user_id': message.from_user.id,
        'text': message.text,
        'date': message.date,
    }
    
    logging.info('Saving message: %s', message_data)

    try:
        # Сохранение сообщения в таблицу "messages"
        await conn.execute('''
            INSERT INTO messages(chat_id, user_id, text, date)
            VALUES($1, $2, $3, $4)
        ''', message_data['chat_id'], message_data['user_id'], message_data['text'], datetime.utcnow())
        logging.info('Message saved successfully.')
    except Exception as e:
        logging.error('Error saving message: %s', e)
    finally:
        await conn.close()  # Закрыть соединение

async def search_messages(chat_id, user_id=None):
    conn = await connect_to_db()
    if conn is None:
        logging.error("Database connection is not established. Cannot search for messages.")
        return []

    query = 'SELECT * FROM messages WHERE chat_id = $1'
    values = [chat_id]

    if user_id is not None:
        query += ' AND user_id = $2'
        values.append(user_id)
    
    try:
        messages = await conn.fetch(query, *v)

