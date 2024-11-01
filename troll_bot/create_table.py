import psycopg2

# Параметры подключения к базе данных на Render.com
connection = psycopg2.connect(
    "postgresql://troll_bot_user:jZA0ASL42zwVsNPVsLVMQ1z5QiLRZXl8@dpg-cshqar68ii6s73bk1dkg-a.oregon-postgres.render.com/troll_bot_db"
)

# Создание курсора для выполнения SQL-запросов
cursor = connection.cursor()

# SQL-запрос для создания таблицы
create_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

# Выполнение запроса
cursor.execute(create_table_query)

# Подтверждение изменений
connection.commit()

# Закрытие соединения
cursor.close()
connection.close()

print("Таблица успешно создана!")
