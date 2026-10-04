import duckdb
import pandas as pd
from pathlib import Path
from utils import upload_to_minio

# ==============================
# PATHS
# ==============================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

print("========== GOLD LAYER ==========")

# ==============================
# CONNECT TO DUCKDB
# ==============================

db_path = DATA_DIR / "olympics.duckdb"
con = duckdb.connect(str(db_path))

try:
    # ==============================
    # LOAD SILVER DATA
    # ==============================

    silver_path = DATA_DIR / "athlete_events_clean.parquet"
    athletes = pd.read_parquet(silver_path)

    print("Athletes loaded")

    con.register("athletes_df", athletes)

    con.execute("""
        CREATE OR REPLACE TABLE athletes AS
        SELECT * FROM athletes_df
    """)

    # ==============================
    # DIMENSION: ATHLETE
    # ==============================

    con.execute("""
        CREATE OR REPLACE TABLE DimAthlete AS
        SELECT
            ID AS athlete_id,
            MAX(Name) AS Name,
            MAX(Sex) AS Sex,
            MAX(Age) AS Age,
            MAX(Height) AS Height,
            MAX(Weight) AS Weight
        FROM athletes
        WHERE ID IS NOT NULL
        GROUP BY ID
    """)

    print("DimAthlete created")

    # ==============================
    # DIMENSION: SPORT
    # ==============================

    con.execute("""
        CREATE OR REPLACE TABLE DimSport AS
        SELECT DISTINCT
            Sport
        FROM athletes
        WHERE Sport IS NOT NULL
    """)

    print("DimSport created")

    # ==============================
    # DIMENSION: OLYMPICS
    # ==============================

    con.execute("""
        CREATE OR REPLACE TABLE DimOlympics AS
        SELECT DISTINCT
            Games,
            Year,
            Season,
            City
        FROM athletes
    """)

    print("DimOlympics created")

    # ==============================
    # DIMENSION: COUNTRY
    # ==============================

    con.execute("""
        CREATE OR REPLACE TABLE DimCountry AS
        SELECT DISTINCT
            NOC,
            Team
        FROM athletes
    """)

    print("DimCountry created")

    # ==============================
    # FACT TABLE: PARTICIPATION
    # ==============================

    con.execute("""
        CREATE OR REPLACE TABLE FactParticipation AS
        SELECT
            ID AS athlete_id,
            Sport,
            NOC,
            Games,
            Medal
        FROM athletes
    """)

    print("FactParticipation created")

    # ==============================
    # LIST TABLES
    # ==============================

    print("\nTables created:")

    tables = con.execute("SHOW TABLES").fetchall()

    for table in tables:
        print("-", table[0])

    # ==============================
    # EXPORT GOLD TABLES TO PARQUET
    # ==============================

    print("\nExporting Gold tables...")

    gold_tables = [
        "DimAthlete",
        "DimSport",
        "DimOlympics",
        "DimCountry",
        "FactParticipation",
    ]

    for table in gold_tables:
        output_path = DATA_DIR / f"{table}.parquet"

        con.execute(
            f"COPY {table} TO '{output_path.as_posix()}' (FORMAT PARQUET)"
        )

        print(f"{output_path.name} created")

    print("Parquet files created")


    print("Start/configure MinIO before enabling uploads.")


    for table in gold_tables:
         file_path = DATA_DIR / f"{table}.parquet"
         upload_to_minio(str(file_path), "gold")

    print("\n========== GOLD COMPLETED ==========")

finally:
    con.close()

