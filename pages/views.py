# pages/views.py (TESTE DIRETO COM BOTO3)

import boto3
from botocore.exceptions import ClientError
from django.http import HttpResponse
import os
import logging

logger = logging.getLogger(__name__)

def home_view(request):
    logger.warning("--- INICIANDO TESTE DE UPLOAD DIRETO COM BOTO3 ---")

    # Carrega as credenciais e configurações direto do ambiente
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region_name = os.environ.get('AWS_S3_REGION_NAME')
    bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    object_name = "boto3_direct_test.txt"
    file_content = b"Este e um teste usando boto3 diretamente para validar as credenciais e a conexao."

    # Verifica se todas as variáveis foram carregadas
    if not all([aws_access_key_id, aws_secret_access_key, region_name, bucket_name]):
        error_msg = "ERRO DE CONFIGURACAO: Uma ou mais variaveis de ambiente da AWS nao foram encontradas no Render."
        logger.error(error_msg)
        return HttpResponse(f"<h1>{error_msg}</h1>", status=500)

    logger.info(f"Tentando conectar ao bucket '{bucket_name}' na regiao '{region_name}' com a chave '...{aws_access_key_id[-4:]}'")

    # Cria o cliente S3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    try:
        # Tenta fazer o upload do objeto
        s3_client.put_object(Body=file_content, Bucket=bucket_name, Key=object_name, ACL='public-read')
        
        message = f"<h1>Sucesso com Boto3!</h1><p>O arquivo '{object_name}' foi enviado diretamente para o bucket '{bucket_name}'.<br>Por favor, verifique o console da AWS agora.</p>"
        logger.warning("--- SUCESSO NO UPLOAD DIRETO COM BOTO3 ---")
        return HttpResponse(message)

    except ClientError as e:
        # Captura e exibe o erro exato da AWS, se houver
        error_code = e.response.get("Error", {}).get("Code")
        error_message = e.response.get("Error", {}).get("Message")
        logger.error(f"--- ERRO DO BOTO3: {error_code} ---", exc_info=True)
        logger.error(f"MENSAGEM DE ERRO COMPLETA: {e.response}")
        message = f"<h1>Erro Direto do Boto3</h1><h2>Codigo do Erro: {error_code}</h2><p>Mensagem: {error_message}</p><hr><pre>{e.response}</pre>"
        return HttpResponse(message, status=500)
    
    except Exception as e:
        # Captura qualquer outro erro inesperado
        logger.error("--- ERRO INESPERADO NO TESTE BOTO3 ---", exc_info=True)
        return HttpResponse(f"<h1>Erro Inesperado</h1><pre>{e}</pre>", status=500)