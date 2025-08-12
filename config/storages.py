# config/storages.py
from storages.backends.s3boto3 import S3Boto3Storage

class S3MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

# Este é o nosso storage para arquivos de mídia PRIVADOS
class PrivateMediaStorage(S3Boto3Storage):
    location = 'private_media' # Salva em uma pasta separada no S3
    default_acl = 'private' # A configuração mais importante: torna os arquivos privados
    file_overwrite = False
    custom_domain = False # Garante que as URLs geradas não sejam as de acesso público