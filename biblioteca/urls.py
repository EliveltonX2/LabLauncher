# biblioteca/urls.py
from django.urls import path
from . import views # Vamos criar as views no próximo passo

app_name = 'biblioteca'

urlpatterns = [
    path('', views.BibliotecaLandingView.as_view(), name='landing'),
    path('menu/', views.BookMenuView.as_view(), name='menu'),
    path('book/<int:pk>/view/', views.BookViewerPDFView.as_view(), name='book-viewer'),
    path('book/<int:pk>/data/', views.get_book_pdf_data_view, name='book-pdf-data'),
]