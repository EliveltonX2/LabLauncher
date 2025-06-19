# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Define a configuração de admin para o nosso CustomUser.
    Vamos adicionar nossos campos customizados ('is_approved', 'profile_picture')
    para que apareçam no painel.
    """
    # Adiciona os campos ao formulário de criação de usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_approved', 'profile_picture')}),
    )
    # Adiciona os campos ao formulário de edição de usuário
    fieldsets = UserAdmin.fieldsets + (
        ('Status de Aprovação', {'fields': ('is_approved', 'profile_picture')}),
    )
    # Mostra os campos na lista principal de usuários
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_approved']

# Registra o nosso modelo CustomUser com a nossa configuração customizada
admin.site.register(CustomUser, CustomUserAdmin)