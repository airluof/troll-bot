from flask import Flask
import os
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 5000))  # Используйте PORT из окружения
    app.run(host="0.0.0.0", port=port)  # Слушаем на всех интерфейсах

def keep_alive():
    t = threading.Thread(target=run)
    t.start()
