# pages/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', kaizo_view, name='kaizo_view'), #esta vai ser a pagina da Kaizo
    path('lablauncher/', home_view, name='home'), #esta sera a pagina home do lab launcher
    path('hall-of-fame/', hall_of_fame_view, name='hall-of-fame'),
    path('dashboard/', dashboard_view, name='dashboard'), # <-- Adicione esta linha
    path('<slug:slug>/', StaticPageView.as_view(), name='static_page'),
]