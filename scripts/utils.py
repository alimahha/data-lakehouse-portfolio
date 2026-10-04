import hashlib
from minio import Minio


def calculate_md5(filepath):
    hash_md5 = hashlib.md5()

    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def upload_to_minio(filepath, bucket_name):
    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    object_name = filepath.split("/")[-1]

    client.fput_object(
        bucket_name,
        object_name,
        filepath
    )

    print(f"Uploaded {object_name} to {bucket_name}")