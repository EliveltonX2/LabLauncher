# inventory/urls.py
from django.urls import path
from .views import *

app_name = 'inventory'

urlpatterns = [
    # A URL raiz do nosso app de inventário ('/inventory/') levará para a página de rosto.
    path('', InventoryLandingView.as_view(), name='landing'),
    path('labs/', LaboratorioListView.as_view(), name='lab-list'),
    path('labs/<int:pk>/', LaboratorioDetailView.as_view(), name='lab-detail'),
]