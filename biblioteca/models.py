# biblioteca/models.py
import os
from django.db import models
from django.urls import reverse
from django.conf import settings
from config.storages import S3MediaStorage, PrivateMediaStorage
from django.core.files.storage import FileSystemStorage

# --- LÓGICA DE SELEÇÃO DE STORAGE ---
if os.getenv('USE_S3') == 'TRUE':
    public_storage = S3MediaStorage()
    private_storage = PrivateMediaStorage()
else:
    # Em desenvolvimento, ambos os storages apontam para o sistema de arquivos,
    # mas para pastas diferentes.
    public_storage = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
    private_storage = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT)

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título do Livro")
    author = models.CharField(max_length=200, verbose_name="Autor")
    description = models.TextField(blank=True, verbose_name="Descrição")

    # A imagem da capa será pública, então usamos o storage padrão (que já aponta para o S3 público)
    cover_image = models.ImageField(upload_to='book_covers/', storage=public_storage, verbose_name="Imagem da Capa")

    # O arquivo PDF será privado
    pdf_file = models.FileField(upload_to='private_books/', storage=private_storage, verbose_name="Arquivo PDF")

    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"
        ordering = ['published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # URL para a página do visualizador do livro
        return reverse('biblioteca:book-viewer', kwargs={'pk': self.pk})