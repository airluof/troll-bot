from flask import Flask, request

app = Flask(__name__)

@app.route('/b1871c694b036ae3097c5bf27f8733fcd33d6a1a', methods=['POST'])
def handle_webhook():
    # Здесь можно обрабатывать полученные данные от Telegram
    data = request.get_json()
    print("Получены данные от вебхука:", data)  # Выводим данные в консоль для проверки
    return 'Webhook received', 200

def keep_alive():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    keep_alive()
