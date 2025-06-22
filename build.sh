#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- INICIANDO BUILD SCRIPT DE DEBUG (v2 Corrigido) ---"

echo "--- Passo 1: Instalando dependencias ---"
pip install -r requirements.txt

echo "--- Passo 2: Rodando collectstatic ---"
python manage.py collectstatic --no-input --clear

echo "--- Passo 3: VERIFICANDO STATUS DAS MIGRACOES (ANTES) ---"
# CORREÇÃO: Removido o --no-input
python manage.py showmigrations

echo "--- Passo 4: EXECUTANDO O MIGRATE ---"
python manage.py migrate --no-input

echo "--- Passo 5: VERIFICANDO STATUS DAS MIGRACOES (DEPOIS) ---"
# CORREÇÃO: Removido o --no-input
python manage.py showmigrations

echo "--- Passo 6: Criando superusuario ---"
python manage.py create_superuser_from_env

echo "--- BUILD SCRIPT CONCLUIDO COM SUCESSO! ---"