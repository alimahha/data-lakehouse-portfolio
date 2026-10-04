import pandas as pd
import pyarrow as pa
from deltalake.writer import write_deltalake
from utils import upload_to_minio

print("========== SILVER LAYER ==========")

print("\nProcessing athlete_events.csv...")

athletes = pd.read_csv("../data/athlete_events.csv")

# Remplacer les valeurs manquantes textuelles
athletes.replace(["NA", "NULL"], pd.NA, inplace=True)

athletes["Age"] = pd.to_numeric(athletes["Age"], errors="coerce")
athletes["Height"] = pd.to_numeric(athletes["Height"], errors="coerce")
athletes["Weight"] = pd.to_numeric(athletes["Weight"], errors="coerce")

athletes["Sport"] = athletes["Sport"].str.strip().str.title()
athletes["Team"] = athletes["Team"].str.strip()

athletes.drop_duplicates(inplace=True)

athletes.to_parquet(
    "../data/athlete_events_clean.parquet",
    index=False
)

print("athlete_events_clean.parquet created")

write_deltalake(
    "../data/delta_athletes",
    pa.Table.from_pandas(athletes),
    mode="overwrite"
)

print("delta_athletes created")


print("\nProcessing wikidata_olympic.csv...")

wiki = pd.read_csv("../data/wikidata_olympic.csv")

# Remplacement des valeurs manquantes textuelles
wiki.replace(["NA", "NULL"], pd.NA, inplace=True)

wiki.drop_duplicates(inplace=True)

wiki["athleteLabel"] = wiki["athleteLabel"].str.strip()
wiki["countryLabel"] = wiki["countryLabel"].str.strip()
wiki["sportLabel"] = wiki["sportLabel"].str.strip().str.title()

wiki.to_parquet(
    "../data/wikidata_olympic_clean.parquet",
    index=False
)

print("wikidata_olympic_clean.parquet created")

write_deltalake(
    "../data/delta_wikidata",
    pa.Table.from_pandas(wiki),
    mode="overwrite"
)

print("delta_wikidata created")


print("\nUploading Parquet files to Silver bucket...")

upload_to_minio(
    "../data/athlete_events_clean.parquet",
    "silver"
)

upload_to_minio(
    "../data/wikidata_olympic_clean.parquet",
    "silver"
)

print("\n========== SILVER COMPLETED ==========")