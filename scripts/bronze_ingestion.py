import csv
import os
from utils import calculate_md5, upload_to_minio

FILES = [
    "../data/athlete_events.csv",
    "../data/wikidata_olympic.csv"
]

CHECKSUM_FILE = "../checksums.csv"

existing_checksums = {}

with open(CHECKSUM_FILE, mode="r", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        existing_checksums[row["filename"]] = row["md5"]

updated_checksums = {}

for file in FILES:
    filename = os.path.basename(file)

    current_md5 = calculate_md5(file)

    updated_checksums[filename] = current_md5

    if filename not in existing_checksums:
        print(f"[NEW] {filename} → needs ingestion")
        upload_to_minio(file, "bronze")

    elif existing_checksums[filename] != current_md5:
        print(f"[UPDATED] {filename} → needs ingestion")
        upload_to_minio(file, "bronze")

    else:
        print(f"[SKIP] {filename} → no changes detected")

with open(CHECKSUM_FILE, mode="w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow(["filename", "md5"])

    for filename, md5 in updated_checksums.items():
        writer.writerow([filename, md5])