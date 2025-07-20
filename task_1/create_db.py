import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()  # креди до дб в окремому файлі

def create_db():
    # Визначаємо шлях до скрипта та підключаємося до бази
    base_dir = os.path.dirname(__file__)
    sql_path = os.path.join(base_dir, "tables.sql")

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    with conn:
        with conn.cursor() as cur:
            with open(sql_path, "r") as f:
                sql = f.read()
                cur.execute(sql)


if __name__ == "__main__":
    create_db()