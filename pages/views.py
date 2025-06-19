# pages/views.py (TESTE DE UPLOAD SEM SEPARADOR DE PATH)

from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

def home_view(request):
    logger.warning("--- INICIANDO TESTE DE UPLOAD SEM SEPARADOR DE PATH ---")
    try:
        file_content = b"Teste de upload com nome de objeto simples."
        file = ContentFile(file_content)
        
        # A MUDANÇA CRÍTICA: Salva com um nome simples, sem barras "/"
        object_name_without_path = "teste_final_no_bucket.txt"
        file_name = default_storage.save(object_name_without_path, file)
        
        logger.warning(f"--- SUCESSO (APARENTE)! Django salvou como '{file_name}'. ---")
        return HttpResponse(f"<h1>Teste Concluido!</h1><p>Tentativa de salvar o arquivo como '{file_name}' (sem caminho de pasta).<br>Por favor, verifique a raiz do seu bucket S3 agora.</p>")

    except Exception as e:
        logger.error("--- FALHA NO UPLOAD! ---", exc_info=True)
        return HttpResponse(f"<h1>Erro no Upload</h1><h2>{type(e).__name__}</h2><pre>{e}</pre>", status=500)