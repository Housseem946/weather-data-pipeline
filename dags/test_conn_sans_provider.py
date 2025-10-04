from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
import psycopg2

CONN_ID = "postgres_weather"

def create_and_insert():
    c = BaseHook.get_connection(CONN_ID)
    dsn = {"host": c.host, "port": c.port or 5432, "dbname": c.schema,
           "user": c.login, "password": c.password}
    with psycopg2.connect(**dsn) as cx, cx.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS healthcheck(
              id SERIAL PRIMARY KEY,
              created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        cur.execute("INSERT INTO healthcheck DEFAULT VALUES;")
        cx.commit()

def select_count():
    c = BaseHook.get_connection(CONN_ID)
    dsn = {"host": c.host, "port": c.port or 5432, "dbname": c.schema,
           "user": c.login, "password": c.password}
    with psycopg2.connect(**dsn) as cx, cx.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM healthcheck;")
        print("healthcheck rows =", cur.fetchone()[0])

with DAG(
    dag_id="test_conn_sans_provider",
    start_date=datetime(2024, 1, 1),
    catchup=False,
):
    t1 = PythonOperator(task_id="create_and_insert", python_callable=create_and_insert)
    t2 = PythonOperator(task_id="select_count", python_callable=select_count)
    t1 >> t2
