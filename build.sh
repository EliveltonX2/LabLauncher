#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- INICIANDO BUILD SCRIPT COM RESET DE MIGRATIONS ---"

pip install -r requirements.txt
python manage.py collectstatic --no-input --clear

# --- O RESET ---
# Passo 1: Diz ao banco de produção para "esquecer" o histórico de migrações do app 'catalog'.
# Isso NÃO deleta as tabelas, apenas limpa os registros.
echo "--- Forçando reset do histórico de migrações para o app 'catalog' ---"
python manage.py migrate catalog zero --fake

# Passo 2: Agora, roda o migrate normalmente.
# Ele encontrará o nosso novo arquivo 0001_initial.py e o aplicará,
# criando as tabelas que faltam (PartCategory, etc.).
echo "--- Aplicando todas as migrações a partir de um estado limpo ---"
python manage.py migrate

# Passo 3: Cria o superusuário.
python manage.py create_superuser_from_env

echo "--- BUILD SCRIPT CONCLUÍDO ---"