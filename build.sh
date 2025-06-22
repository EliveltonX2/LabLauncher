#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- INICIANDO BUILD SCRIPT DE REPARO DE MIGRACOES ---"

pip install -r requirements.txt
python manage.py collectstatic --no-input --clear

# --- A CORREÇÃO DEFINITIVA ---
# Este comando diz ao Django: "Para qualquer app que tenha uma migração 'initial'
# mas cujas tabelas já existam no banco, apenas marque a migração como aplicada
# sem tentar criar as tabelas novamente."
echo "--- Rodando --fake-initial para alinhar o banco de dados de produção ---"
python manage.py migrate --fake-initial

echo "--- BUILD SCRIPT DE REPARO CONCLUIDO ---"