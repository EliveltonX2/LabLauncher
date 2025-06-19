# users/management/commands/create_superuser_from_env.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    """
    Comando para criar um superusuário usando variáveis de ambiente.
    Ideal para deploys automatizados onde a interação não é possível.
    """
    help = 'Cria um superusuário a partir das variáveis de ambiente ADMIN_USER, ADMIN_EMAIL, ADMIN_PASSWORD.'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USER')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR(
                'Por favor, defina as variáveis de ambiente ADMIN_USER, ADMIN_EMAIL e ADMIN_PASSWORD.'
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                f'Superusuário com o nome de usuário "{username}" já existe.'
            ))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(
                f'Superusuário "{username}" criado com sucesso!'
            ))
