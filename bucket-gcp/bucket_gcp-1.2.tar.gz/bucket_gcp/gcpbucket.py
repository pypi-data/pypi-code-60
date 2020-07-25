
from google.cloud import storage

from google.oauth2 import service_account


from django.http import HttpResponse
import pandas as pd
class Bucket:

        
    def upload_to_bucket(blob_name, path_to_file, bucket_name, credentials):
        try:
            # Explicitly use service account credentials
            # by specifying the private key file.
            storage_client = service_account.Credentials.from_service_account_info(credentials)
            storage_client = storage.Client(credentials=storage_client, project="shopdev-gcp")
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(path_to_file)
            return True, blob.public_url
        except Exception as e:
            return False, str(e.args)

    def read_file(file_name, bucket_name,storage_name,credentials_file):
        storage_client = service_account.Credentials.from_service_account_info(credentials_file)
        storage_client = storage.Client(credentials=storage_client, project="shopdev-gcp")
        # storage_client = storage.Client.from_service_account_json(
        #     credentials_file)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.get_blob(file_name)
        blob.download_to_filename(storage_name)
        print("name ",blob.name)
        return storage_name