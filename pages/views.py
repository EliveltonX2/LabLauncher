# pages/views.py (TESTE FINAL: ONDE VOCÊ ESTÁ SALVANDO?)

from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

def home_view(request):
    logger.warning("--- INICIANDO TESTE DE LOCALIZACAO DE ARQUIVO ---")
    try:
        file_content = b"Teste para descobrir o caminho do arquivo."
        file = ContentFile(file_content)
        object_name = "onde_voce_foi.txt"
        
        # 1. Salva o arquivo como antes
        file_name_saved = default_storage.save(object_name, file)
        logger.info(f"Storage diz que salvou o arquivo como: {file_name_saved}")

        # 2. Tenta obter o caminho absoluto do arquivo no sistema de arquivos
        try:
            absolute_path = default_storage.path(file_name_saved)
            # SE CHEGOU AQUI, O ARQUIVO FOI SALVO LOCALMENTE
            logger.error(f"!!! PROBLEMA CONFIRMADO: ARQUIVO SALVO LOCALMENTE EM: {absolute_path} !!!")
            message = (f"<h1>Problema Encontrado e Confirmado!</h1>"
                       f"<p>O Django esta usando o FileSystemStorage e salvando o arquivo localmente no servidor do Render, e nao no S3.</p>"
                       f"<p>Caminho absoluto no servidor: <strong>{absolute_path}</strong></p>")
            status_code = 200

        except NotImplementedError:
            # SE CHEGOU AQUI, O STORAGE É S3, COMO DEVERIA SER
            logger.warning("!!! BOAS NOTICIAS: O storage e S3 (metodo .path() nao implementado). O upload foi enviado. !!!")
            message = (f"<h1>Boas Noticias!</h1>"
                       f"<p>O storage e S3, pois o metodo .path() gerou o erro esperado.</p>"
                       f"<p>Isso significa que o arquivo '{file_name_saved}' foi enviado para a AWS, mas não está visível por um problema de permissão final.</p>")
            status_code = 200

        except Exception as e_path:
             # Captura qualquer outro erro inesperado
             logger.error(f"Erro inesperado ao chamar .path(): {e_path}", exc_info=True)
             message = f"<h1>Erro Inesperado ao Chamar .path()</h1><pre>{e_path}</pre>"
             status_code = 500

        return HttpResponse(message, status=status_code)

    except Exception as e_save:
        logger.error("--- FALHA AO SALVAR O ARQUIVO! ---", exc_info=True)
        return HttpResponse(f"<h1>Erro ao Salvar o Arquivo</h1><h2>{type(e_save).__name__}</h2><pre>{e_save}</pre>", status=500)