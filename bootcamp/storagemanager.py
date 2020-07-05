from django.core.files.storage import Storage
from django.core.files.base import File
from django.utils.deconstruct import deconstructible
from google.cloud import storage
import os

@deconstructible
class GoogleCloudStorage(Storage):

    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_name = "inthernet-bucket"
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

    def _save(self, name, content: File):
        blob = self.bucket.blob(name)

        blob.upload_from_file(content.file)

        blob.make_public()
        print(
            "File {} uploaded.".format(
                name
            )
        )
        return name

    def _open(self, name, mode='rb'):
        blob = self.bucket.blob(name)
        blob.download_to_filename(name)
        return File(open(name, mode))

    def exists(self, name):
        return self.bucket.blob(name).exists()

    def delete(self, name):
        try:
            self.bucket.blob(name).delete()
        except Exception:
            return

    def listdir(self, path):
        return

    def size(self, name):
        return

    def url(self, name):
        return self.bucket.blob(name).public_url

    def generate_filename(self, filename: str):
        if filename.find('resumes\\') == 0:
            filename.replace('\\','/',1)
        return filename
