#!/usr/bin/env bash
# exit on error
set -o errexit

# "Chef do Render, por favor, instale todas as ferramentas da minha lista"
pip install -r requirements.txt

# "Agora, junte todos os meus arquivos de design (CSS, JS) em uma única pasta"
python manage.py collectstatic --no-input

# "Por fim, prepare o banco de dados com as tabelas mais recentes"
python manage.py migrate

python manage.py create_superuser_from_env