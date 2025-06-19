from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    """
    Modelo de usuário customizado que herda do padrão do Django.
    Adicionamos campos para foto de perfil e status de aprovação.
    """
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


def __str__(self):
        return self.username