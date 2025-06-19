# config/storages.py (VERSÃO DE DEBUG DETALHADO)

from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Determina qual classe base será usada
if settings.USE_S3:
    logger.warning(">>> settings.USE_S3 E VERDADEIRO. A classe base sera S3Boto3Storage. <<<")
    StorageBaseClass = S3Boto3Storage
else:
    logger.warning(">>> settings.USE_S3 E FALSO. A classe base sera FileSystemStorage. <<<")
    StorageBaseClass = FileSystemStorage

class MediaStorage(StorageBaseClass):
    # Este método é chamado toda vez que o Django cria uma instância do nosso storage.
    def __init__(self, *args, **kwargs):
        logger.warning(f"--- INICIALIZANDO A CLASSE MediaStorage (que herda de {StorageBaseClass.__name__}) ---")

        # Se estivermos usando S3, definimos os atributos específicos do S3 aqui.
        if settings.USE_S3:
            kwargs['bucket_name'] = settings.AWS_STORAGE_BUCKET_NAME
            kwargs['location'] = 'media'
            kwargs['default_acl'] = 'public-read'
            kwargs['file_overwrite'] = False
            logger.info(f"Configuracoes S3 passadas para o __init__: bucket={kwargs.get('bucket_name')}, location={kwargs.get('location')}")

        # Chama o __init__ da classe pai (S3Boto3Storage ou FileSystemStorage)
        super().__init__(*args, **kwargs)
        logger.warning("--- MediaStorage INICIALIZADA COM SUCESSO. ---")