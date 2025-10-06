## 🌦️ Weather Data Pipeline

Ce projet met en place un pipeline de données automatisé pour collecter, stocker et transformer des données météorologiques en temps réel à partir de l’API Weatherstack
.
Il s’appuie sur un stack moderne de Data Engineering :

- **Airflow** pour l’orchestration

- **PostgreSQL** pour le stockage brut

- **DBT** pour la transformation et la modélisation des données

- Docker & Docker Compose pour l’environnement isolé et reproductible

L’objectif est de démontrer une architecture complète de Data Pipeline ETL (Extract → Load → Transform) industrialisable.

### 🛠️ Stack Technique

- Python 3.12

- Apache Airflow 2.x (via Astronomer CLI)

- PostgreSQL 14

- pgAdmin 4 (interface SQL)

- DBT Core + dbt-postgres

- Docker / Docker Compose

### 📂 Structure du projet

```bash
weather-data-pipeline/
│── dags/                     # DAGs Airflow (extraction & orchestration)
│   ├── extract_weather.py    # Script d’extraction API -> Postgres
│   ├── extract_weather_dag.py# DAG Airflow qui orchestre l’extraction
│── include/                  # Scripts auxiliaires Python
│── plugins/                  # (si besoin de custom operators)
│── tests/                    # Tests unitaires
│── dbt_project/              # Projet DBT (modèles + seeds)
│── docker-compose.override.yml
│── Dockerfile
│── requirements.txt
│── airflow_settings.yaml     # Connexions Airflow
│── .env                      # Variables d’environnement (API keys, etc.)
└── README.md
```
### ⚙️ Installation & Lancement

1️⃣ Cloner le repo
```bash
git clone https://github.com/Housseem946/weather-data-pipeline.git
cd weather-data-pipeline
```
2️⃣ Lancer Docker + Airflow

```bash
astro dev start
```
Airflow UI sera dispo sur : http://localhost:8080

pgAdmin : http://localhost:5050

### 🔑 Configuration des Variables Airflow

Dans Airflow UI (Admin > Variables) :

WEATHERSTACK_API_KEY → ta clé API Weatherstack

CITIES → liste des villes à suivre (ex dans mon cas : "Paris,London,Madrid")

Dans Admin > Connections :

Connexion postgres_weather → Postgres cible (weather_db)

### 📊 Fonctionnement du Pipeline

- Étape 1 : Extraction (API → Postgres)

Appel de l’API Weatherstack pour chaque ville

Insertion dans la table brute raw_weather au format JSONB

- Étape 2 : Transformation (DBT)

Modélisation en tables analytiques (stg_weather, mart_weather)

Nettoyage des colonnes & historisation des mesures

- Étape 3 : Visualisation (optionnel)

Connexion de Postgres à Grafana / Metabase pour analyser les tendances météo

### 👩‍💻 Authored By Me 
