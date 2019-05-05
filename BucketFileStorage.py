from google.cloud import storage

def create_file_structure():
    storage_client = storage.Client()

    # Check if the buckets have already been created
    b = storage_client.list_buckets()
    required_number_buckets = 2
    required_buckets = ["cs378_final_converted_videos", "cs378_final_raw_videos"]
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
        converted = storage_client.create_bucket("cs378_final_converted_videos")
        raw = storage_client.create_bucket("cs378_final_raw_videos")
