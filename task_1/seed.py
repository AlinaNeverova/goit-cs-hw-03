import psycopg2
import os
from faker import Faker
from random import randint
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()  # креди

NUMBER_OF_USERS = 10
NUMBER_OF_TASKS = 50
STATUSES = ['new', 'in progress', 'completed']

fake = Faker()

# Генеруємо фейкові імена та унікальні мейли для користувачів
def generate_users(n):
    return [(fake.name(), fake.unique.email()) for _ in range(n)]

# Генеруємо задачі
def generate_tasks(n, user_count):
    now = datetime.now() # щоб створити рандомні дати для задач, а не дату створення таблиці
    tasks = []
    for _ in range(n):
        created_at = now - timedelta(days=randint(0, 30)) # беремо останні 30 днів
        tasks.append((
            fake.sentence(nb_words=6),
            fake.text(max_nb_chars=200),
            randint(1, len(STATUSES)),
            randint(1, user_count),
            created_at
        ))    
    return tasks

# коннектимось до бази й заливаємо рандомні дані в таблиці
def insert_data_to_db(users, statuses, tasks):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    with conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO users (fullname, email) VALUES (%s, %s);",
                users
            )
            cur.executemany(
                "INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
                [(s,) for s in statuses]
            )
            cur.executemany(
                "INSERT INTO tasks (title, description, status_id, user_id, created_at) VALUES (%s, %s, %s, %s, %s);",
                tasks
            )


if __name__ == "__main__":
    users = generate_users(NUMBER_OF_USERS)
    tasks = generate_tasks(NUMBER_OF_TASKS, len(users))
    insert_data_to_db(users, STATUSES, tasks)