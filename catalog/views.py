# catalog/views.py

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Part, Project, Category
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
    context_object_name = 'parts'
    paginate_by = 10

    def get_queryset(self):
        """
        Esta é a função principal. Ela constrói a busca no banco de dados.
        """
        # Começa com todos os objetos aprovados
        queryset = super().get_queryset().filter(status='approved')

        # Pega os parâmetros da URL
        search_query = self.request.GET.get('q')
        category_query = self.request.GET.get('category')

        # Filtro de busca por texto
        if search_query:
            # Usa Q objects para fazer uma busca OR no nome E na descrição
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )

        # Filtro por categoria
        if category_query:
            queryset = queryset.filter(category__id=category_query)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        """
        Esta função adiciona dados extras ao contexto que será enviado ao template.
        """
        # Pega o contexto existente da classe pai
        context = super().get_context_data(**kwargs)
        # Adiciona a lista de todas as categorias ao contexto
        context['categories'] = Category.objects.all()
        return context

    

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
        """
        Adiciona a lógica de busca e filtro para os projetos.
        """
        queryset = super().get_queryset().filter(status='approved')

        search_query = self.request.GET.get('q')
        category_query = self.request.GET.get('category')

        if search_query:
            # Busca no título E na descrição do projeto
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )

        if category_query:
            queryset = queryset.filter(category__id=category_query)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        """
        Adiciona a lista de categorias ao contexto para o dropdown de filtro.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'catalog/project_detail.html'
    context_object_name = 'project'


