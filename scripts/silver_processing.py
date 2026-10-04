import pandas as pd
import pyarrow as pa
from deltalake.writer import write_deltalake
from utils import upload_to_minio
from transformations import clean_athletes, clean_wikidata

print("========== SILVER LAYER ==========")

print("\nProcessing athlete_events.csv...")

athletes = pd.read_csv("../data/athlete_events.csv")

athletes = clean_athletes(athletes)

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

wiki = clean_wikidata(wiki)

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