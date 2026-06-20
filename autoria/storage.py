import cloudinary
import cloudinary.uploader
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class CloudinaryStorage(Storage):
    def __init__(self, folder=''):
        self.folder = folder

    def _save(self, name, content):
        # Завантажуємо файл в Cloudinary
        path = f"{self.folder}/{name}" if self.folder else name
        response = cloudinary.uploader.upload(
            content,
            public_id=path.rsplit('.', 1)[0],
            overwrite=True,
            resource_type='image',
        )
        return response['public_id']

    def url(self, name):
        return cloudinary.CloudinaryImage(name).build_url()

    def exists(self, name):
        return False

    def delete(self, name):
        cloudinary.uploader.destroy(name)