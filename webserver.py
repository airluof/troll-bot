from flask import Flask, request
import logging

app = Flask(__name__)

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

@app.route('/<path:webhook_path>', methods=['POST'])
def handle_webhook(webhook_path):
    data = request.get_json()
    log.info("Получены данные от вебхука: %s", data)  # Логируем полученные данные
    log.info("Тип данных: %s", type(data))  # Логируем тип данных
    # Здесь вы можете добавить дополнительную логику обработки данных
    return 'Webhook received', 200

def keep_alive():
    app.run(host='0.0.0.0', port=5000)  # Запускаем Flask-сервер на всех интерфейсах

if __name__ == "__main__":
    keep_alive()  # Запускаем Flask-сервер для поддержания активности
