# from config.settings import *
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
from datetime import datetime

today= datetime.now().strftime("%Y-%m-%d")

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING=os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER = "bronze"

if not AZURE_STORAGE_CONNECTION_STRING:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable not set")

def upload_blob_file(file_path, blob_path):
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(container=CONTAINER)
    with open(file_path, "r", encoding='utf-8') as f:
        data = f.read()
        container_client.upload_blob(
            name=blob_path,
            data=data,
            overwrite=True
        )
        print(f"Uploaded: {blob_path}")

def upload_all():
    print("Uploading is about to begin...")
    
    # works both locally and inside Docker
    BASE_DIR = os.environ.get('AIRFLOW_HOME',
               os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    local_folder = os.path.join(BASE_DIR, 'data', 'bronze', 'justjoin', today)

    files = [f for f in os.listdir(local_folder) if f.endswith(".json")]
    total = len(files)

    for index, filename in enumerate(files, start=1):
        local_path = os.path.join(local_folder, filename)
        blob_name = f"justjoin/{today}/{filename}"

        upload_blob_file(local_path, blob_name)
        print(f"Progress: {index}/{total}")


