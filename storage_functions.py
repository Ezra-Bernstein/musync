from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = ".appspot.com"
    # source_file_name = "local/path/to/file" "tmp/" + filename
    # destination_blob_name = "storage-object-name" "class/filename"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def transfer_files(bucket_name, classcode):
    """Transfers all files in class to /tmp"""
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)
    count = 0
    for blob in blobs:
        if blob.name[:len(classcode)] == classcode:
            blob.download_to_filename("tmp/"+classcode+"/"+blob.name[len(classcode)+1:])
            
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print("Downloaded",count,"files from class",classname)
