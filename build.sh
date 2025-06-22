#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- INICIANDO BUILD SCRIPT FINAL ---"

pip install -r requirements.txt
python manage.py collectstatic --no-input --clear

# --- A CORREÇÃO ---
# Passo 1: Finge que a migração inicial já foi aplicada.
# Isso alinha o histórico do Django com as tabelas que já existem no banco do Render.
echo "--- Rodando FAKE INITIAL migrate para o app 'catalog' ---"
python manage.py migrate catalog --fake-initial

# Passo 2: Agora, roda o migrate normalmente para aplicar quaisquer outras migrações pendentes.
echo "--- Rodando migrate normal para o restante dos apps ---"
python manage.py migrate

# Passo 3: Cria o superusuário.
python manage.py create_superuser_from_env

echo "--- BUILD SCRIPT CONCLUÍDO ---"