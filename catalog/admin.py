# catalog/admin.py

from django.contrib import admin
from .models import Category, Part, Project

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Configuração de admin para o modelo Category.
    """
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} # Preenche o slug automaticamente a partir do nome

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    """
    Configuração de admin para o modelo Part.
    """
    list_display = ('name', 'author', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'author')
    search_fields = ('name', 'description', 'author__username')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Configuração de admin para o modelo Project.
    """
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'author')
    search_fields = ('title', 'description', 'author__username')