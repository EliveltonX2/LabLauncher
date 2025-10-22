# pages/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', kaizo_view, name='kaizo_view'), #esta vai ser a pagina da Kaizo
    path('sobre/', sobre_view, name='sobre'),
    path('termos/', termos_view, name='termos'),
    path('politica/', politica_view, name='politica'),
    path('contato/', contato_view, name='contato'),
    path('lablauncher/', home_view, name='home'), #esta sera a pagina home do lab launcher
    path('hall-of-fame/', hall_of_fame_view, name='hall-of-fame'),
    path('dashboard/', dashboard_view, name='dashboard'), # <-- Adicione esta linha
    path('<slug:slug>/', StaticPageView.as_view(), name='static_page'),
]