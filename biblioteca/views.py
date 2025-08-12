# biblioteca/views.py
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Book

class BibliotecaLandingView(TemplateView):
    """Apresenta a página de rosto da biblioteca."""
    template_name = "biblioteca/landing.html"

class BookMenuView(ListView):
    """Mostra a lista de livros disponíveis."""
    model = Book
    template_name = "biblioteca/menu.html"
    context_object_name = "books" # Nome da lista de livros no template


class BookViewerPDFView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "biblioteca/book_viewer.html"
    context_object_name = "book"

@login_required # Garante que apenas usuários logados possam acessar os dados
def get_book_pdf_data_view(request, pk):
    """
    Esta view segura entrega os dados brutos de um arquivo PDF.
    """
    book = get_object_or_404(Book, pk=pk)

    # Aqui você poderia adicionar lógicas extras (ex: o usuário pagou por este livro?)

    try:
        # Abre o arquivo (seja local ou do S3) e o envia como resposta
        return FileResponse(book.pdf_file.open('rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()