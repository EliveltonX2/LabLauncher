# inventory/views.py
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
import json

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

# --- NOVA VIEW PARA O MAPA ---
class LaboratorioMapView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/lab_map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Pega todos os laboratórios que têm localização definida
        labs_with_location = Laboratorio.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)

        # 2. Prepara os dados para o JSON
        labs_data = []
        for lab in labs_with_location:
            labs_data.append({
                'id': lab.id,
                'name': lab.name,
                'lat': lab.latitude,
                'lng': lab.longitude,
                'status': lab.status,
                'status_display': lab.get_status_display(), # Pega o nome legível do status
                'lab_type': lab.lab_type.name if lab.lab_type else 'Sem Categoria',
                'detail_url': lab.get_absolute_url(),
                # --- NOVOS DADOS PARA O POPUP ---
                'endereco': f"{lab.endereco}, {lab.numero}" if lab.endereco and lab.numero else lab.endereco,
                'telefone': lab.telefone,
                'description': lab.description,
            })


        # 3. Converte os dados para uma string JSON segura
        context['labs_json'] = json.dumps(labs_data)

        # 4. Pega todos os tipos de laboratório para o filtro
        context['lab_types'] = LaboratorioType.objects.all()

        return context