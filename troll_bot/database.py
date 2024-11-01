import os
import logging
import asyncpg  # Убедитесь, что этот пакет установлен

# Установка уровня логирования
logging.basicConfig(level=logging.DEBUG)

# Подключение к PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    logging.error("DATABASE_URL is not set.")
else:
    logging.info("DATABASE_URL is set: %s", DATABASE_URL)

async def create_connection():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        logging.info("Successfully connected to PostgreSQL.")
        return conn
    except Exception as e:
        logging.error("Failed to connect to PostgreSQL: %s", e)
        return None

async def create_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT NOT NULL,
        user_id BIGINT NOT NULL,
        text TEXT,
        date TIMESTAMP
    );
    """
    try:
        await conn.execute(query)
        logging.info("Table 'messages' created successfully.")
    except Exception as e:
        logging.error("Error creating table: %s", e)

async def save_message(conn, message):
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
        query = """
        INSERT INTO messages(chat_id, user_id, text, date)
        VALUES($1, $2, $3, $4)
        """
        await conn.execute(query, message_data['chat_id'], message_data['user_id'], message_data['text'], message_data['date'])
        logging.info('Message saved successfully.')
    except Exception as e:
        logging.error('Error saving message: %s', e)

async def search_messages(conn, chat_id, user_id=None):
    if conn is None:
        logging.error("Database connection is not established. Cannot search for messages.")
        return []

    query = "SELECT * FROM messages WHERE chat_id = $1"
    if user_id is not None:
        query += " AND user_id = $2"

    try:
        if user_id is not None:
            messages = await conn.fetch(query, chat_id, user_id)
        else:
            messages = await conn.fetch(query, chat_id)
        return messages  # Возвращаем все найденные сообщения
    except Exception as e:
        logging.error('Error searching messages: %s', e)
        return []

async def main():
    conn = await create_connection()
    if conn:
        await create_table(conn)  # Создание таблицы при запуске
        # Здесь можете использовать функции save_message и search_messages
        # Пример: await save_message(conn, some_message)
        # Пример: await search_messages(conn, some_chat_id)
        await conn.close()  # Закрытие соединения с базой данных

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
