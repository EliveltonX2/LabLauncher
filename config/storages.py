# LabLauncher/storages.py
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class StaticStorage(S3Boto3Storage):
    location = settings.AWS_LOCATION_STATIC
    default_acl = 'public-read'

class MediaStorage(S3Boto3Storage):
    location = settings.AWS_LOCATION_MEDIA
    default_acl = 'public-read'
    file_overwrite = False # Não sobrescrever arquivos com o mesmo nome