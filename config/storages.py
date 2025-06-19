# config/storages.py (VERSÃO ROBUSTA COM LAZYOBJECT)

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.functional import LazyObject
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(LazyObject):
    def _setup(self):
        """
        Este método é chamado apenas na primeira vez que o storage é acessado.
        Neste ponto, temos certeza de que todas as settings já foram carregadas.
        """

        # Se USE_S3 for True, o objeto de storage real será o S3Boto3Storage.
        self._wrapped = S3Boto3Storage()

# Criamos uma instância "preguiçosa" que será importada no settings.py
media_storage = MediaStorage()