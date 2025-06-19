# users/models.py (CÓDIGO CORRIGIDO)
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from config.storages import S3MediaStorage

s3_storage = S3MediaStorage()

class CustomUser(AbstractUser):
    # Nossos campos customizados
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True,
        verbose_name='Foto do Perfil'
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name='Aprovado pela Curadoria',
        help_text='Indica se o usuário foi aprovado para acessar o conteúdo.'
    )

    # Campos para resolver o conflito
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set", # Nome único para o acesso reverso
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set", # Nome único para o acesso reverso
        related_query_name="user",
    )

    def __str__(self):
        return self.username