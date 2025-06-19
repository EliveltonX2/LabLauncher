# catalog/views.py

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import *
from .forms import *

class PartCreateView(LoginRequiredMixin, CreateView):
    model = Part
    form_class = PartForm
    template_name = 'catalog/part_form.html'
    success_url = reverse_lazy('home') # Redireciona para a homepage após o sucesso

    def form_valid(self, form):
        """
        Este método é chamado quando o formulário enviado é válido.
        """
        # Associa o autor da peça ao usuário que está logado.
        form.instance.author = self.request.user
        # Define o status inicial como 'em revisão'.
        form.instance.status = 'in_review'
        # Continua o processo normal de salvar o formulário.
        return super().form_valid(form)
    
class PartListView(ListView):
    model = Part
    template_name = 'catalog/part_list.html'
    context_object_name = 'parts' # Nome da variável no template
    paginate_by = 10 # (Opcional) Mostra 10 peças por página

    def get_queryset(self):
        """
        Sobrescreve o método padrão para buscar apenas as peças
        com status 'approved'.
        """
        return Part.objects.filter(status='approved').order_by('-created_at')
    

class PartDetailView(DetailView):
    model = Part
    template_name = 'catalog/part_detail.html'
    context_object_name = 'part' # Nome do objeto no template


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'catalog/project_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'in_review'
        return super().form_valid(form)

class ProjectListView(ListView):
    model = Project
    template_name = 'catalog/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.filter(status='approved').order_by('-created_at')

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'catalog/project_detail.html'
    context_object_name = 'project'