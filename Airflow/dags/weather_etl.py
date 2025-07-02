from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import os

# Dictionnaire des villes avec leurs coordonnées
CITIES = {
    "Paris": {"lat": 48.85, "lon": 2.35},
    "Londres": {"lat": 51.51, "lon": -0.13},
    "Berlin": {"lat": 52.52, "lon": 13.40}
}

# Chemin vers le fichier de sortie
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "weather_data.csv")
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

def extract_weather():
    results = []
    for city, coords in CITIES.items():
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current_weather=true"
        response = requests.get(url)
        data = response.json().get("current_weather", {})
        results.append({
            "city": city,
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": data.get("temperature"),
            "windspeed": data.get("windspeed"),
            "weathercode": data.get("weathercode")
        })
    df = pd.DataFrame(results)
    df.to_csv("/tmp/weather_temp.csv", index=False)

def load_weather():
    if not os.path.exists("/tmp/weather_temp.csv"):
        return
    new_df = pd.read_csv("/tmp/weather_temp.csv")
    
    if os.path.exists(DATA_PATH):
        old_df = pd.read_csv(DATA_PATH)
        combined = pd.concat([old_df, new_df])
        
        # Supprimer les doublons selon les colonnes de données météo
        combined = combined.drop_duplicates(
            subset=["city", "temperature", "windspeed", "weathercode"],
            keep="last"
        )
    else:
        combined = new_df

    combined.to_csv(DATA_PATH, index=False)


# Définition du DAG
with DAG(
    dag_id="weather_etl_daily",
    schedule="0 8 * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["weather", "ETL"]
) as dag:


    extract = PythonOperator(
        task_id="extract_weather_data",
        python_callable=extract_weather
    )

    load = PythonOperator(
        task_id="load_weather_data",
        python_callable=load_weather
    )

    extract >> load
