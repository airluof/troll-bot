import os
import logging
from pymongo import MongoClient  # Убедитесь, что этот пакет установлен

# Установка уровня логирования
logging.basicConfig(level=logging.DEBUG)

# Подключение к MongoDB
MONGODB_URI = os.getenv('MONGODB_URI')

if not MONGODB_URI:
    logging.error("MONGODB_URI is not set.")
else:
    logging.info("MONGODB_URI is set: %s", MONGODB_URI)

def create_connection():
    try:
        client = MongoClient(MONGODB_URI)
        db = client['troll_bot_db']  # Замените на имя вашей базы данных
        logging.info("Successfully connected to MongoDB.")
        return db
    except Exception as e:
        logging.error("Failed to connect to MongoDB: %s", e)
        return None

def create_collection(db):
    try:
        collection = db['messages']  # Замените на имя вашей коллекции
        logging.info("Collection 'messages' created successfully.")
        return collection
    except Exception as e:
        logging.error("Error creating collection: %s", e)
        return None

def save_message(collection, message):
    if collection is None:
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
        collection.insert_one(message_data)
        logging.info('Message saved successfully.')
    except Exception as e:
        logging.error('Error saving message: %s', e)

def search_messages(collection, chat_id, user_id=None):
    if collection is None:
        logging.error("Database connection is not established. Cannot search for messages.")
        return []

    query = {'chat_id': chat_id}
    if user_id is not None:
        query['user_id'] = user_id

    try:
        messages = list(collection.find(query))  # Возвращаем все найденные сообщения
        return messages
    except Exception as e:
        logging.error('Error searching messages: %s', e)
        return []

def main():
    db = create_connection()
    if db:
        collection = create_collection(db)  # Создание коллекции
        # Здесь можете использовать функции save_message и search_messages
        # Пример: save_message(collection, some_message)
        # Пример: messages = search_messages(collection, some_chat_id)
        
        # Закрытие соединения с MongoDB
        db.client.close()

if __name__ == "__main__":
    main()
