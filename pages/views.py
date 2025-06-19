# pages/views.py (TESTE DE LOCALIZACAO)
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

def home_view(request):
    logger.warning("--- INICIANDO TESTE DE LOCALIZACAO (TENTATIVA FINAL) ---")
    try:
        file_content = b"Tentando descobrir o storage usado."
        file_name = default_storage.save("localizacao.txt", ContentFile(file_content))
        absolute_path = default_storage.path(file_name)
        message = f"PROBLEMA PERSISTE: Salvou localmente em {absolute_path}"
        logger.error(message)
        return HttpResponse(f"<h1>{message}</h1>", status=500)
    except NotImplementedError:
        message = "BOAS NOTICIAS: O storage e S3, o upload foi enviado."
        logger.warning(message)
        return HttpResponse(f"<h1>{message}</h1>")
    except Exception as e:
        message = f"ERRO INESPERADO: {e}"
        logger.error(message, exc_info=True)
        return HttpResponse(f"<h1>{message}</h1>", status=500)