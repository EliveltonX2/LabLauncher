# pages/views.py (CÓDIGO DE DEBUG TEMPORÁRIO)

from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

def home_view(request):
    logger.warning("--- VIEW DE TESTE: Iniciando upload para S3. ---")
    try:
        file_content = b"Teste final de upload para debug."
        file = ContentFile(file_content)
        file_name = default_storage.save("debug/final_test.txt", file)

        logger.warning(f"--- VIEW DE TESTE: Sucesso aparente! Django salvou como '{file_name}'. ---")
        return HttpResponse(f"<h1>Sucesso (Aparente)!</h1><p>Django acredita que salvou o arquivo '{file_name}'. Verifique os logs para detalhes da inicializacao do storage.</p>")

    except Exception as e:
        logger.error("--- VIEW DE TESTE: FALHA NO UPLOAD! ---", exc_info=True)
        return HttpResponse(f"<h1>Erro no Upload</h1><h2>{type(e).__name__}</h2><pre>{e}</pre>", status=500)