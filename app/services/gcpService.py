
# [START storage_list_buckets]
from google.cloud import storage


async def uploadImage(imageStream, imageId):
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    bucket = storage_client.get_bucket("predictions_vd")

    blob = bucket.blob("prediction" + imageId)
    blob.upload_from_string(imageStream.getvalue(), content_type="image/png")
# [END storage_list_buckets]
    return "Image uploaded"

if __name__ == "__main__":
    list_buckets()


async def getImage(imageId):
    client = storage.Client()  # Implicit environ set-up
    bucket = client.bucket("predictions_vd")
    blob = bucket.blob("prediction" + imageId)
    url_lifetime = 3600  # Seconds in an hour
    servingUrl = blob.public_url
    return servingUrl
