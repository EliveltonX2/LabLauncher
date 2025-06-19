# pages/urls.py
from django.urls import path
from .views import home_view

urlpatterns = [
    # Quando a URL for vazia (a página inicial), chame a função home_view
    path('', home_view, name='home'),
]