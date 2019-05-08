from google.cloud import storage
import requests
import json
import os
import boto3
import botocore
import subprocess
from subprocess import run, PIPE

#Creds
PROJECT_ID = os.environ.get("PROJECT_ID", None)
aws_access_key_id = os.environ.get("aws_access_key_id", None)
aws_secret_access_key = os.environ.get("aws_secret_access_key", None)

def obtain_credentials_from_aws_s3():
    # s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    # BUCKET_NAME = "cs378-final-project-cloud-storage-bucket-creds"
    # OBJECT_NAME = "cs378-final-project-media-5360efad6b3d.json"
    # FILE_NAME = "C:/cs378-final-project-media-5360efad6b3d.json"
    # s3.download_file(BUCKET_NAME, OBJECT_NAME, FILE_NAME)

    BUCKET_NAME = 'cs378-final-project-cloud-storage-bucket-creds' # replace with your bucket name
    KEY = 'cs378-final-project-media-5360efad6b3d.json' # replace with your object key

    s3 = boto3.resource('s3')

    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, KEY)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise e



def set_credentials_from_aws_s3():
    cwd = os.getcwd()
    print("cwd: \t\t{}".format(cwd))
    for root, dirs, files in os.walk(cwd):
        for filename in files:
            print("Filename: \t{}".format(str(os.path.join(root, filename))))
        for dirname in dirs:
            print("Directory: \t{}".format(str(os.path.join(root, dirname))))

    FILE_NAME = cwd + "\\" + "cs378-final-project-media-5360efad6b3d.json"
    print("FILE_NAME: ", FILE_NAME)
    p = subprocess.run(["set", "GOOGLE_APPLICATION_CREDENTIALS", "=", FILE_NAME], check=True, stdout=PIPE, input='\n')


#Get creds for GOOGLE_APPLICATION_CREDENTIALS
# obtain_credentials_from_aws_s3()
# set_credentials_from_aws_s3()


"""
Creates the file structure for the Buckets
If we don't currently have the required bucket structure, it deletes all the current buckets,
then adds all the buckets
"""
def create_file_structure():
    storage_client = storage.Client()

    found_buckets = []
    for bucket in storage_client.list_buckets():
        found_buckets.append(bucket.name)
    print("Found buckets: ", found_buckets)

    #Just do it, don't worry about idempotency
    required_buckets = ["cs378_final_converted_videos", "cs378_final_raw_videos"]
    for bucket_name in required_buckets:
        if bucket_name not in found_buckets:
            storage_client.create_bucket(bucket_name)


"""
Attempts to get an object with name filename from bucket called bucket
Return the object if successful, None if unsuccessful
Note that blob.name will give "filename.fileext"

Returns it in a variable
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
Downloads it, in FILE form
"""
def download_object(source_blob_name, bucket_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))


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

"""
Copies an object, then puts it into the destination_bucket
"""
def copy_and_write_object(source_bucket_name, blob_name, dest_bucket_name):
    """Copies a blob from one bucket to another with a new name."""
    storage_client = storage.Client()
    source_bucket = storage_client.get_bucket(source_bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.get_bucket(dest_bucket_name)

    new_blob = source_bucket.copy_blob(
        source_blob, destination_bucket, blob_name)

    print('Blob {} in source bucket {} copied to blob {} in dest bucket {}.'.format(
        source_blob.name, source_bucket.name, new_blob.name,
        destination_bucket.name))

"""
Delete object from bucket
"""
def delete_object(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))
