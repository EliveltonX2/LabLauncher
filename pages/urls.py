# pages/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'), # <-- Adicione esta linha
    path('<slug:slug>/', StaticPageView.as_view(), name='static_page'),
]