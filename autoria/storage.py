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
            public_id=path.rsplit('.', 1)[0],  # без розширення
            overwrite=True,
            resource_type='image',
        )
        return response['public_id']

    def url(self, name):
        # Повертаємо URL з Cloudinary CDN
        return cloudinary.CloudinaryImage(name).build_url()

    def exists(self, name):
        return False  # Завжди дозволяємо перезапис

    def delete(self, name):
        cloudinary.uploader.destroy(name)