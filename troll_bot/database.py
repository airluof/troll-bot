import os
import logging
from pymongo import MongoClient

# Установка уровня логирования
logging.basicConfig(level=logging.DEBUG)

# Подключение к MongoDB
MONGO_URI = os.getenv('MONGO_URI')

if not MONGO_URI:
    logging.error("MONGO_URI is not set.")
else:
    logging.info("MONGO_URI is set: %s", MONGO_URI)

client = MongoClient(MONGO_URI)
db = client['troll-bot']

def save_message(message):
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
        # Сохранение сообщения в коллекцию "messages"
        db.messages.insert_one(message_data)
        logging.info('Message saved successfully.')
    except Exception as e:
        logging.error('Error saving message: %s', e)

def search_messages(chat_id, user_id=None):
    query = {'chat_id': chat_id}
    if user_id is not None:
        query['user_id'] = user_id
    
    try:
        messages = db.messages.find(query)
        return list(messages)  # Возвращаем все найденные сообщения в виде списка
    except Exception as e:
        logging.error('Error searching messages: %s', e)
        return []
