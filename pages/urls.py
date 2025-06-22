# pages/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('hall-of-fame/', hall_of_fame_view, name='hall-of-fame'),
    path('dashboard/', dashboard_view, name='dashboard'), # <-- Adicione esta linha
    path('<slug:slug>/', StaticPageView.as_view(), name='static_page'),
]