#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- INICIANDO BUILD SCRIPT COM SINCRONIZACAO DE BANCO ---"

pip install -r requirements.txt
python manage.py collectstatic --no-input --clear

# --- A SINCRONIZAÇÃO ---

# Passo 1: Aplica todas as migrações de TODOS OS OUTROS apps primeiro.
echo "--- Aplicando migracoes de outros apps (auth, admin, etc.) ---"
python manage.py migrate --exclude catalog

# Passo 2: Agora, força o alinhamento do histórico do app 'catalog'.
# Ele vai marcar 0001_initial como aplicada sem tentar criar as tabelas que já existem.
echo "--- Rodando --fake-initial especificamente para o app 'catalog' ---"
python manage.py migrate catalog --fake-initial

# Passo 3: Cria o superusuário.
python manage.py create_superuser_from_env

echo "--- BUILD SCRIPT DE SINCRONIZACAO CONCLUIDO ---"