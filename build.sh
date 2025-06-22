#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- INICIANDO BUILD SCRIPT DE DEBUG ---"

echo "--- Passo 1: Instalando dependencias do requirements.txt ---"
pip install -r requirements.txt

echo "--- Passo 2: Rodando collectstatic ---"
# Adicionamos a flag --clear para garantir que a pasta de estáticos esteja limpa
python manage.py collectstatic --no-input --clear

echo "--- Passo 3: VERIFICANDO STATUS DAS MIGRACOES (ANTES) ---"
# Este comando nos mostra quais migrações foram aplicadas ([X]) e quais não foram ([ ])
python manage.py showmigrations --no-input

echo "--- Passo 4: EXECUTANDO O MIGRATE ---"
# Este é o comando que suspeitamos que está falhando
python manage.py migrate --no-input

echo "--- Passo 5: VERIFICANDO STATUS DAS MIGRACOES (DEPOIS) ---"
# Verificamos novamente para ver se o status mudou
python manage.py showmigrations --no-input

echo "--- Passo 6: Criando superusuario ---"
python manage.py create_superuser_from_env

echo "--- BUILD SCRIPT CONCLUIDO COM SUCESSO! ---"