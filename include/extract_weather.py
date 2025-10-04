import os, json, time
import requests
import psycopg2
from airflow.hooks.base import BaseHook
from airflow.models import Variable

CONN_ID = os.getenv("POSTGRES_CONN_ID", "postgres_weather")
API_KEY = Variable.get("WEATHERSTACK_API_KEY")  ## os.getenv("WEATHERSTACK_API_KEY") 
CITIES = Variable.get("CITIES", default_var="Paris,London,Madrid").split(",")

DDL_RAW = """
CREATE TABLE IF NOT EXISTS raw_weather(
  ingested_at TIMESTAMP NOT NULL,
  city TEXT NOT NULL,
  payload JSONB NOT NULL
);
"""

def get_pg_dsn():
    conn = BaseHook.get_connection(CONN_ID)
    return {
        "host": conn.host,
        "port": conn.port or 5432,
        "dbname": conn.schema,
        "user": conn.login,
        "password": conn.password,
    }

def fetch_city(city: str) -> dict:
    url = "http://api.weatherstack.com/current"
    params = {"access_key": API_KEY, "query": city}
    r = requests.get(url, params=params, timeout=25)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise RuntimeError(f"Weatherstack error for {city}: {data['error']}")
    return data

def main():
    assert API_KEY, "Airflow Variable WEATHERSTACK_API_KEY manquante"
    dsn = get_pg_dsn()
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    with psycopg2.connect(**dsn) as cx, cx.cursor() as cur:
        cur.execute(DDL_RAW)
        for city in [c.strip() for c in CITIES if c.strip()]:
            payload = fetch_city(city)
            cur.execute(
                "INSERT INTO raw_weather(ingested_at, city, payload) VALUES (%s,%s,%s)",
                (now, city, json.dumps(payload)),
            )
        cx.commit()

if __name__ == "__main__":
    main()
