from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import include.extract_weather as extract_weather  # ton script (il doit être dans PYTHONPATH ou dans le dossier plugins/include)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="extract_weather_dag",
    default_args=default_args,
    description="Extraction météo via Weatherstack → Postgres",
    schedule_interval="@hourly",  # exécution chaque heure
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["weather", "postgres"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_weather_task",
        python_callable=extract_weather.main,
    )

    extract_task
