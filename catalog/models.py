from django.db import models
from django.conf import settings # Para referenciar o CustomUser
from ckeditor_uploader.fields import RichTextUploadingField
from config.storages import S3MediaStorage


# Cria uma instância do nosso storage para ser usada nos campos
s3_storage = S3MediaStorage()

# Create your models here.
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
    STATUS_CHOICES = (
        ('in_review', 'Em Revisão'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    )

    name = models.CharField(max_length=200, verbose_name='Nome da Peça')
    description = models.TextField(verbose_name='Descrição')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Categoria')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Não deletar a peça se o autor for removido
        null=True,
        verbose_name='Autor'
    )
    stl_file = models.FileField(upload_to='parts_stl/', verbose_name='Arquivo STL')
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
    STATUS_CHOICES = (
        ('in_review', 'Em Revisão'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    )

    title = models.CharField(max_length=255, verbose_name='Título do Projeto')
    # Usando o campo do CKEditor para uma descrição rica
    description = RichTextUploadingField(verbose_name='Descrição Detalhada')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Autor'
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Categoria')
    # Relação Muitos-para-Muitos: um projeto pode usar várias peças.
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