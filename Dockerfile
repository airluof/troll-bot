FROM python:3.9

# Установка необходимых системных пакетов
RUN apt-get update && \
    apt-get install -y espeak vorbis-tools && \
    rm -rf /var/lib/apt/lists/*

# Копируем код приложения
ADD . /troll-bot
WORKDIR /troll-bot

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Указываем порт, на котором будет работать приложение
EXPOSE 5000

# Указываем команду для запуска приложения
ENTRYPOINT ["python", "-m", "troll_bot"]
