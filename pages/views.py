# pages/views.py (CÓDIGO DE DEBUG TEMPORÁRIO)

from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

def home_view(request):
    logger.warning("--- INICIANDO TESTE DE UPLOAD DIRETO PARA O S3 ---")
    try:
        # 1. Cria um conteúdo de arquivo em memória
        file_content = b"Este e um teste de upload para debug do S3."

        # 2. Cria um objeto de arquivo do Django
        file = ContentFile(file_content)

        # 3. Tenta salvar o arquivo usando o storage padrão (que deve ser o S3)
        file_name = default_storage.save("debug/s3_direct_test.txt", file)

        # 4. Se chegou aqui, o upload funcionou
        logger.warning(f"--- SUCESSO! Arquivo '{file_name}' salvo no S3. ---")
        return HttpResponse(f"<h1>Sucesso!</h1><p>O arquivo de teste '{file_name}' foi salvo com sucesso no seu bucket S3.</p>")

    except Exception as e:
        # 5. Se qualquer exceção ocorrer, ela será capturada aqui
        logger.error("--- FALHA NO UPLOAD DIRETO PARA O S3! ---", exc_info=True)
        return HttpResponse(f"<h1>Erro no Upload para o S3</h1><h2>{type(e).__name__}</h2><pre>{e}</pre>", status=500)