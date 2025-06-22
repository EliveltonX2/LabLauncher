# catalog/admin.py

from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Part, Project
import random

#ACTIONS

@admin.action(description="Duplicar Peças selecionadas para teste")
def duplicate_parts(modeladmin, request, queryset):
    """
    Ação que duplica os objetos Part selecionados 5 vezes cada.
    """
    total_new_parts = 0
    all_categories = list(Category.objects.all()) # Pega todas as categorias uma vez

    for part in queryset:
        for i in range(5): # Cria 5 cópias para cada peça selecionada
            original_pk = part.pk
            part.pk = None  # Truque do Django: definir a PK como None força a criação de um novo objeto
            part.name = f"{part.name} (Cópia {total_new_parts + 1})"

            # Opcional: Atribui uma categoria aleatória para variar os dados
            if all_categories:
                part.category = random.choice(all_categories)

            part.save()
            total_new_parts += 1

        # Restaura a PK do objeto original no loop para evitar efeitos colaterais
        part.pk = original_pk

    # Mostra uma mensagem de sucesso para o usuário no admin
    modeladmin.message_user(
        request,
        f"{total_new_parts} novas peças foram criadas com sucesso.",
    )


#REGISTRANDO MODELOS
@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    mptt_level_indent = 20 # Define a indentação visual da árvore


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    """
    Configuração de admin para o modelo Part.
    """
    list_display = ('name', 'author', 'category', 'status', 'is_hall_of_fame')
    list_filter = ('status', 'category', 'author', 'is_hall_of_fame') 
    list_editable = ('status', 'is_hall_of_fame') 
    search_fields = ('name', 'description', 'author__username')
    actions = [duplicate_parts]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Configuração de admin para o modelo Project.
    """
    list_display = ('title', 'author', 'category', 'status', 'created_at', 'is_hall_of_fame')
    list_filter = ('status', 'category', 'author', 'is_hall_of_fame')
    list_editable = ('status', 'is_hall_of_fame')
    search_fields = ('title', 'description', 'author__username')