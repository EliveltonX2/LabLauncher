# config/storages.py (VERSÃO FINAL E CORRETA)

from storages.backends.s3boto3 import S3Boto3Storage

class S3MediaStorage(S3Boto3Storage):
    # A configuração virá toda do settings.py,
    # mas podemos definir valores padrão aqui.
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False