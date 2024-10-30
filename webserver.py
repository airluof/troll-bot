from flask import Flask, request
import logging

app = Flask(__name__)

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

@app.route('/<path:webhook_path>', methods=['POST'])
def handle_webhook(webhook_path):
    log.info("Webhook path: %s", webhook_path)  # Логируем путь вебхука
    data = request.get_json()
    log.info("Получены данные от вебхука: %s", data)  # Логируем полученные данные
    if data:
        log.info("Данные успешно получены.")
    else:
        log.warning("Получены пустые данные.")
    return 'Webhook received', 200

def keep_alive():
    app.run(host='0.0.0.0', port=5000)  # Запуск Flask-сервера на всех адресах
