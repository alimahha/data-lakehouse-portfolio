import duckdb
import pandas as pd
from utils import upload_to_minio

print("========== GOLD LAYER ==========")


con = duckdb.connect("../data/olympics.duckdb")


athletes = pd.read_parquet("../data/athlete_events_clean.parquet")

print("Athletes loaded")

con.register("athletes_df", athletes)

con.execute("""
CREATE OR REPLACE TABLE athletes AS
SELECT * FROM athletes_df
""")


con.execute("""
CREATE OR REPLACE TABLE DimAthlete AS
SELECT DISTINCT
    ID AS athlete_id,
    Name,
    Sex,
    Age,
    Height,
    Weight
FROM athletes
""")

print("DimAthlete created")


con.execute("""
CREATE OR REPLACE TABLE DimSport AS
SELECT DISTINCT
    Sport
FROM athletes
""")

print("DimSport created")


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

con.execute("""
CREATE OR REPLACE TABLE DimCountry AS
SELECT DISTINCT
    NOC,
    Team
FROM athletes
""")

print("DimCountry created")

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

print("\nTables created:")

tables = con.execute("SHOW TABLES").fetchall()

for table in tables:
    print("-", table[0])

print("\nExporting Gold tables...")

con.execute("""
COPY DimAthlete
TO '../data/DimAthlete.parquet'
(FORMAT PARQUET)
""")

con.execute("""
COPY DimSport
TO '../data/DimSport.parquet'
(FORMAT PARQUET)
""")

con.execute("""
COPY DimOlympics
TO '../data/DimOlympics.parquet'
(FORMAT PARQUET)
""")

con.execute("""
COPY DimCountry
TO '../data/DimCountry.parquet'
(FORMAT PARQUET)
""")

con.execute("""
COPY FactParticipation
TO '../data/FactParticipation.parquet'
(FORMAT PARQUET)
""")

print("Parquet files created")

print("\nUploading Gold files to MinIO...")

upload_to_minio("../data/DimAthlete.parquet", "gold")
upload_to_minio("../data/DimSport.parquet", "gold")
upload_to_minio("../data/DimOlympics.parquet", "gold")
upload_to_minio("../data/DimCountry.parquet", "gold")
upload_to_minio("../data/FactParticipation.parquet", "gold")

print("\n========== GOLD COMPLETED ==========")

con.close()