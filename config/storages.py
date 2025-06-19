# config/storages.py

from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class MediaStorage(S3Boto3Storage if settings.USE_S3 else FileSystemStorage):
    if settings.USE_S3:
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        location = 'media'
        default_acl = 'public-read'
        file_overwrite = False
    else:
        # Configuração para FileSystemStorage em desenvolvimento
        location = settings.MEDIA_ROOT
        base_url = settings.MEDIA_URL