# catalog/models.py (COM LÓGICA DE STORAGE INTERNA)

import os
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from ckeditor_uploader.fields import RichTextUploadingField
from config.storages import S3MediaStorage

# --- LÓGICA DE SELEÇÃO DE STORAGE ---
# Esta decisão é tomada aqui, no momento em que o Django carrega este arquivo.
if os.getenv('USE_S3') == 'TRUE':
    # Em produção (Render), usa nossa classe S3.
    storage_para_usar = S3MediaStorage()
    print("--- LOG DE DEBUG (models.py): Usando S3MediaStorage ---")
else:
    # Localmente, usa o FileSystemStorage padrão do Django.
    storage_para_usar = FileSystemStorage()
    print("--- LOG DE DEBUG (models.py): Usando FileSystemStorage ---")


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    slug = models.SlugField(max_length=120, unique=True, help_text='Versão do nome otimizada para URLs.')
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']
    def __str__(self):
        return self.name


class Part(models.Model):
    STATUS_CHOICES = (('in_review', 'Em Revisão'), ('approved', 'Aprovado'), ('rejected', 'Rejeitado'))
    name = models.CharField(max_length=200, verbose_name='Nome da Peça')
    description = models.TextField(verbose_name='Descrição')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Categoria')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Autor')

    # O campo agora usa a variável que definimos acima
    stl_file = models.FileField(upload_to='parts_stl/', storage=storage_para_usar, verbose_name='Arquivo STL')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='in_review', verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')
    class Meta:
        verbose_name = 'Peça'
        verbose_name_plural = 'Peças'
        ordering = ['-created_at']
    def __str__(self):
        return self.name


class Project(models.Model):
    # ... (O modelo Project pode continuar igual) ...
    STATUS_CHOICES = (('in_review', 'Em Revisão'), ('approved', 'Aprovado'), ('rejected', 'Rejeitado'))
    title = models.CharField(max_length=255, verbose_name='Título do Projeto')
    description = RichTextUploadingField(verbose_name='Descrição Detalhada')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Autor')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Categoria')
    parts_used = models.ManyToManyField(Part, blank=True, verbose_name='Peças Utilizadas')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='in_review', verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')
    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ['-created_at']
    def __str__(self):
        return self.title