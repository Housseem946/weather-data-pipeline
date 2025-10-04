from datetime import datetime
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

CONN_ID = "postgres_weather"

with DAG(
    dag_id="test_postgres_conn_sql",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id=CONN_ID,
        sql="""
        CREATE TABLE IF NOT EXISTS healthcheck(
          id SERIAL PRIMARY KEY,
          created_at TIMESTAMP DEFAULT NOW()
        );
        """,
    )
    insert_row = SQLExecuteQueryOperator(
        task_id="insert_row",
        conn_id=CONN_ID,
        sql="INSERT INTO healthcheck DEFAULT VALUES;",
    )
    select_count = SQLExecuteQueryOperator(
        task_id="select_count",
        conn_id=CONN_ID,
        sql="SELECT COUNT(*) FROM healthcheck;",
    )
    create_table >> insert_row >> select_count
