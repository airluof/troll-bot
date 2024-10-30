from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"  # Простой ответ на корневой маршрут

def run():
    app.run(host='0.0.0.0', port=5000)

def keep_alive():
    thread = Thread(target=run)
    thread.start()
