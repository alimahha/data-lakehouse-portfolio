# 🏅 Data Lakehouse & Data Engineering — Olympic Data

## 📌 Présentation

Ce projet académique met en œuvre un pipeline **Data Engineering de bout en bout** autour de données relatives aux Jeux Olympiques.

L'objectif est de construire une architecture de type **Data Lakehouse** suivant le principe de la **Medallion Architecture**, organisée en trois couches :

**Bronze → Silver → Gold**

Le projet couvre plusieurs étapes d'une chaîne Data :

- ingestion des données ;
- nettoyage et transformation ;
- modélisation analytique ;
- stockage au format Parquet ;
- requêtage SQL avec DuckDB ;
- stockage objet avec MinIO ;
- contrôles de qualité des données ;
- tests automatisés avec Pytest ;
- intégration continue avec GitHub Actions.

La couche Gold produit un modèle analytique structuré autour de dimensions et d'une table de faits, destiné à être exploité par des outils d'analyse et de visualisation.

---

# 🏗️ Architecture

Le projet suit une architecture **Medallion** en trois couches.

```text
                         SOURCES DE DONNÉES
                                │
                                ▼
                    ┌─────────────────────┐
                    │       BRONZE        │
                    │   Données brutes    │
                    │                     │
                    │ athlete_events.csv  │
                    │ wikidata_olympic.csv│
                    └──────────┬──────────┘
                               │
                               │ Nettoyage
                               │ Transformation
                               ▼
                    ┌─────────────────────┐
                    │       SILVER        │
                    │ Données nettoyées   │
                    │                     │
                    │ Parquet             │
                    │ Contrôles qualité   │
                    └──────────┬──────────┘
                               │
                               │ Modélisation
                               │ analytique
                               ▼
                    ┌─────────────────────┐
                    │        GOLD         │
                    │ Données analytiques │
                    │                     │
                    │ DimAthlete          │
                    │ DimSport            │
                    │ DimOlympics         │
                    │ DimCountry          │
                    │ FactParticipation   │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
          ┌─────────────┐             ┌─────────────┐
          │   DuckDB    │             │    MinIO    │
          │ SQL /       │             │ Object      │
          │ Analytics   │             │ Storage     │
          └─────────────┘             └─────────────┘
                                            │
                                            ▼
                                      Power BI
                                     (à venir)
```

---

# 🥉 Bronze — Données brutes

La couche **Bronze** constitue le point d'entrée du pipeline.

Elle contient les données sources avant les principales transformations.

Les principales sources utilisées sont :

- `athlete_events.csv`
- `wikidata_olympic.csv`

Cette couche permet de conserver les données dans un état proche de leur forme originale et de disposer d'une base pour les traitements suivants.

Les données peuvent également être stockées dans le bucket `bronze` de MinIO.

---

# 🥈 Silver — Données nettoyées

La couche **Silver** contient les données après les premières opérations de nettoyage et de transformation.

Les traitements comprennent notamment :

- nettoyage des données ;
- traitement des valeurs manquantes ;
- contrôle des types ;
- traitement des doublons ;
- préparation des données pour la modélisation analytique.

Les données Silver sont stockées au format **Parquet**, adapté aux traitements analytiques.

Les fichiers principaux sont notamment :

```text
athlete_events_clean.parquet
wikidata_olympic_clean.parquet
```

---

# 🥇 Gold — Données analytiques

La couche **Gold** constitue la couche destinée à l'analyse.

Les données sont organisées selon une logique de **modèle dimensionnel**, avec plusieurs tables de dimensions et une table de faits.

### Dimensions

| Table | Description |
|---|---|
| `DimAthlete` | Informations sur les athlètes |
| `DimSport` | Informations sur les sports |
| `DimOlympics` | Informations sur les éditions olympiques |
| `DimCountry` | Informations sur les pays |

### Table de faits

| Table | Description |
|---|---|
| `FactParticipation` | Informations sur les participations des athlètes |

Cette organisation facilite les requêtes analytiques et prépare les données à une utilisation dans un outil de Business Intelligence.

---

# 🗄️ DuckDB, Parquet et MinIO

Le projet combine plusieurs technologies complémentaires.

## Parquet

Le format **Parquet** est utilisé pour stocker les données Silver et Gold.

Il permet notamment :

- un stockage orienté colonnes ;
- une bonne efficacité pour les traitements analytiques ;
- la conservation des types de données ;
- une intégration simple avec Pandas et DuckDB.

## DuckDB

**DuckDB** est utilisé comme moteur SQL analytique local.

Il permet notamment de :

- réaliser les transformations SQL ;
- créer les tables Gold ;
- effectuer des agrégations ;
- interroger les données Parquet.

La base DuckDB utilisée par le projet est :

```text
data/olympics.duckdb
```

## MinIO

**MinIO** est utilisé comme stockage objet compatible avec l'écosystème S3.

Le projet utilise trois buckets correspondant aux différentes couches :

```text
bronze
silver
gold
```

Les résultats de la couche Gold sont notamment stockés dans le bucket `gold` :

```text
gold/
├── DimAthlete.parquet
├── DimSport.parquet
├── DimOlympics.parquet
├── DimCountry.parquet
└── FactParticipation.parquet
```

---

# 🧪 Tests et qualité des données

La qualité des données est contrôlée automatiquement avec **Pytest**.

Les tests couvrent notamment :

- présence des colonnes obligatoires ;
- détection des doublons ;
- contrôle des types de colonnes ;
- vérification que les données ne sont pas vides ;
- contrôle de l'unicité des identifiants ;
- contrôles sur les fichiers Parquet.

Les tests Parquet utilisent des données de test temporaires afin de pouvoir être exécutés dans un environnement CI sans dépendre des fichiers générés localement.

### Exécuter les tests

```bash
python3 -m pytest -v
```

---

# ⚙️ CI — GitHub Actions

Le projet utilise **GitHub Actions** pour automatiser l'exécution des tests.

Le workflow est déclenché lors :

- d'un `push` ;
- d'une `pull request`.

L'environnement CI installe notamment :

```text
Python
Pandas
Pytest
PyArrow
DuckDB
```

Puis exécute :

```bash
python -m pytest -v
```

Le projet utilise également un workflow Git basé sur les branches et les Pull Requests :

```text
main
 │
 └── feature/...
       │
       ├── développement
       ├── tests
       └── commit
             │
             ▼
       Pull Request
             │
             ▼
       GitHub Actions
             │
          Tests OK
             │
             ▼
           main
```

---

# 🛠️ Technologies utilisées

| Technologie | Utilisation |
|---|---|
| **Python** | Développement du pipeline |
| **Pandas** | Manipulation et transformation des données |
| **SQL** | Transformations et analyses |
| **DuckDB** | Moteur analytique et modélisation |
| **Parquet** | Stockage des données analytiques |
| **MinIO** | Stockage objet compatible S3 |
| **Pytest** | Tests automatisés |
| **PyArrow** | Support du format Parquet |
| **Git / GitHub** | Gestion du code source |
| **GitHub Actions** | Intégration continue |
| **Power BI** | Visualisation — à venir |

---

# 📁 Structure du projet

```text
data-lakehouse-portfolio/
│
├── data/
│   ├── athlete_events.csv
│   ├── wikidata_olympic.csv
│   ├── athlete_events_clean.parquet
│   ├── wikidata_olympic_clean.parquet
│   └── olympics.duckdb
│
├── scripts/
│   ├── bronze_ingestion.py
│   ├── silver_processing.py
│   ├── gold_processing.py
│   ├── transformations.py
│   ├── analytics_queries.py
│   ├── queries.sql
│   └── utils.py
│
├── tests/
│   ├── test_transformations.py
│   ├── test_data_quality.py
│   └── test_parquet_quality.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── .gitignore
└── README.md
```

> Les fichiers Parquet et DuckDB générés localement ne sont pas destinés à être versionnés dans Git. Les résultats générés sont notamment stockés dans MinIO.

---

# 🚀 Installation

## Prérequis

Le projet nécessite :

- Python 3 ;
- Git ;
- un serveur MinIO ;
- les dépendances Python du projet.

## 1. Cloner le projet

```bash
git clone https://github.com/alimahha/data-lakehouse-portfolio.git
cd data-lakehouse-portfolio
```

## 2. Créer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Installer les dépendances

```bash
python -m pip install --upgrade pip
pip install pandas pyarrow duckdb pytest minio
```

---

# 🗃️ Configuration de MinIO

Le projet utilise trois buckets :

```text
bronze
silver
gold
```

Avec le client MinIO (`mc`), ils peuvent être créés avec :

```bash
mc mb local/bronze
mc mb local/silver
mc mb local/gold
```

Vérifier les buckets :

```bash
mc ls local
```

Le serveur MinIO doit être démarré avant l'exécution des traitements nécessitant le stockage objet.

---

# ▶️ Exécution du pipeline

Les différents traitements sont organisés dans le dossier `scripts/`.

## Bronze

```bash
python3 scripts/bronze_ingestion.py
```

## Silver

```bash
python3 scripts/silver_processing.py
```

## Gold

```bash
python3 scripts/gold_processing.py
```

Le traitement Gold génère notamment :

```text
DimAthlete.parquet
DimSport.parquet
DimOlympics.parquet
DimCountry.parquet
FactParticipation.parquet
```

Ces fichiers sont ensuite envoyés dans le bucket `gold` de MinIO.

---

# 🧪 Exécuter les tests

Pour exécuter l'ensemble des tests :

```bash
python3 -m pytest -v
```

---

# 📊 Analyse et visualisation

La couche Gold constitue la base analytique du projet.

Les données peuvent être exploitées avec :

- DuckDB ;
- SQL ;
- Pandas ;
- Power BI.

### Power BI — prochaine évolution

Une couche de visualisation sera ajoutée afin de permettre l'analyse :

- des participations olympiques ;
- des athlètes ;
- des sports ;
- des pays ;
- des médailles ;
- de l'évolution des participations selon les éditions.

---

# 🎯 Objectifs du projet

Ce projet permet de mettre en pratique plusieurs compétences en Data Engineering :

- conception d'un pipeline de données ;
- architecture Medallion ;
- ingestion et transformation de données ;
- Python et SQL ;
- stockage au format Parquet ;
- moteur analytique DuckDB ;
- stockage objet avec MinIO ;
- modélisation dimensionnelle ;
- tests de qualité des données ;
- intégration continue avec GitHub Actions ;
- préparation des données pour la visualisation.

---

# 👤 Auteurs

**Ali Mahha**

Projet académique — Data Lakehouse & Data Engineering
