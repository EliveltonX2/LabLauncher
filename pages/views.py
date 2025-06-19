# pages/views.py (CÓDIGO DE DEBUG AVANÇADO)

from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings # Importa as settings
import logging

logger = logging.getLogger(__name__)

def home_view(request):
    # ETAPA DE INSPEÇÃO
    logger.warning("--- INSPECIONANDO O STORAGE PADRAO (default_storage) ---")
    try:
        storage_class = type(default_storage)
        storage_class_name = storage_class.__name__
        logger.info(f"CLASSE DE STORAGE SENDO USADA: {storage_class}")
        logger.info(f"NOME DA CLASSE: {storage_class_name}")

        # Se for o nosso storage S3, ele terá um atributo 'bucket_name'
        if hasattr(default_storage, 'bucket_name'):
            logger.info(f"NOME DO BUCKET DENTRO DO STORAGE: {default_storage.bucket_name}")
        else:
            logger.warning("O objeto de storage NAO tem o atributo 'bucket_name'.")
        
        # Verifica as settings diretamente para comparação
        default_file_storage_setting = settings.DEFAULT_FILE_STORAGE
        logger.info(f"SETTING 'DEFAULT_FILE_STORAGE' APONTA PARA: '{default_file_storage_setting}'")

        if default_file_storage_setting != 'config.storages.MediaStorage':
             logger.error("ALERTA! A setting DEFAULT_FILE_STORAGE NAO esta apontando para nossa classe MediaStorage!")

    except Exception as e:
        logger.error(f"Erro ao inspecionar o storage: {e}", exc_info=True)
    
    # ETAPA DE TESTE DE UPLOAD
    logger.warning("--- INICIANDO TESTE DE UPLOAD ---")
    try:
        file_content = b"Este e o terceiro teste de upload."
        file = ContentFile(file_content)
        file_name = default_storage.save("debug/s3_inspection_test.txt", file)
        
        logger.warning(f"--- SUCESSO (APARENTE)! Django acredita ter salvo o arquivo '{file_name}'. ---")
        return HttpResponse(f"<h1>Sucesso (Aparente)!</h1><p>O Django acredita que salvou o arquivo '{file_name}'.<br>Verifique os logs para a inspecao da classe de storage usada.</p>")

    except Exception as e:
        logger.error("--- FALHA NO UPLOAD! ---", exc_info=True)
        return HttpResponse(f"<h1>Erro no Upload</h1><h2>{type(e).__name__}</h2><pre>{e}</pre>", status=500)