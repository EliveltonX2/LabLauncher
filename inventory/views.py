# inventory/views.py
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

class InventoryLandingView(TemplateView):
    template_name = "inventory/inventory_landing.html"


# 1. VIEW PARA LISTAR TODOS OS LABORATÓRIOS
class LaboratorioListView(LoginRequiredMixin, ListView):
    model = Laboratorio
    template_name = 'inventory/lab_list.html'
    context_object_name = 'labs' # Nome da variável no template
    paginate_by = 12 # Mostra 12 laboratórios por página


# 2. VIEW PARA VER OS DETALHES DE UM LABORATÓRIO
class LaboratorioDetailView(LoginRequiredMixin, DetailView):
    model = Laboratorio
    template_name = 'inventory/lab_detail.html'
    context_object_name = 'lab' # Nome do objeto no template