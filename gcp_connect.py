from google.cloud import storage

# GCP Bucket connection to the stage area.
def bucket_obj(project_name, bucket_name):
    storage_client = storage.Client(project=project_name)
    return storage_client.get_bucket(bucket_name)

def blob_read(bucket, blob_path, filename, mode_type):
    return bucket.get_blob(blob_path + filename).open(mode=mode_type).read()

def blob_open(bucket, blob_path, filename, mode_type):
    return bucket.blob(blob_path + filename).open(mode=mode_type)

def blob_create(bucket, blob_path, filename):
    return bucket.blob(blob_path + filename)