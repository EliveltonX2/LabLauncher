# config/storages.py -> Versão Simplificada

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaStorage(S3Boto3Storage):
    # A localização dos arquivos de mídia dentro do bucket
    location = 'media'