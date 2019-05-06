from google.cloud import storage
import requests
import json
import os


#Creds
GCP_CS378_MASTER_ADMIN_API_KEY = os.environ.get("GCP_CS378_MASTER_ADMIN_API_KEY", None)

"""
Creates the file structure for the Buckets
If we don't currently have the required bucket structure, it deletes all the current buckets,
then adds all the buckets
"""
def create_file_structure():
    storage_client = storage.Client()

    # Check if the buckets have already been created
    b = storage_client.list_buckets()
    required_buckets = ["cs378_final_converted_videos", "cs378_final_raw_videos", "trim_completed", "trim_staging"]
    required_number_buckets = len(required_buckets)
    num_buckets = 0
    found_buckets = []
    for bucket in storage_client.list_buckets():
        found_buckets.append(bucket.name)
        num_buckets+=1
    found_buckets.sort()

    print("num_buckets: {}, found_buckets: {}".format(num_buckets, found_buckets))

    #If we haven't created the buckets yet, create them
    if num_buckets != required_number_buckets or found_buckets != required_buckets:
        # Delete all the current buckets, for idempotency
        for bucket in storage_client.list_buckets():
            bucket.delete()

        # Create buckets with the appropriate file directory structure
        for bucket_name in required_buckets:
            storage_client.create_bucket(bucket_name)


"""
Attempts to get an object with name filename from bucket called bucket
Return the object if successful, None if unsuccessful

Note that blob.name will give "filename.fileext"
"""
def get_object_from_bucket(filename, bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()
    file = None
    for blob in blobs:
        print(blob.name)
        if blob.name == filename:
            file = blob
    return file
    # response = None
    # try:
    #     query = "https://www.googleapis.com/storage/v1/b/" + bucket + "/o/" + filename + "&key=" + GCP_CS378_MASTER_ADMIN_API_KEY
    #     raw = requests.get(query)
    #     response = raw
    #     print(raw.json())
    # except Exception as e:
    #     print(e)
    # return response


"""
Uploads an object to the bucket
"""
def upload_object(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to bucket {} with dest filename{}.'.format(
        source_file_name, bucket_name,
        destination_blob_name))
