# pages/models.py

from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

class StaticPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(unique=True, help_text="Usado na URL da página. Ex: 'sobre-nos'. Use apenas letras, números e hifens.")
    content = RichTextUploadingField(verbose_name="Conteúdo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Página Estática"
        verbose_name_plural = "Páginas Estáticas"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('static_page', kwargs={'slug': self.slug})