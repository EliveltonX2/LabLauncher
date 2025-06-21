# pages/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required # Para proteger a view
from catalog.models import Part, Project
from .models import StaticPage # Para buscar os dados
from django.views.generic import TemplateView
from django.views.generic import DetailView

def home_view(request):
    return render(request, 'pages/home.html', {})

@login_required # Garante que apenas usuários logados acessem esta página
def dashboard_view(request):
    # Busca as peças do usuário logado
    user_parts = Part.objects.filter(author=request.user).order_by('-created_at')

    # Busca os projetos do usuário logado
    user_projects = Project.objects.filter(author=request.user).order_by('-created_at')

    # Prepara o contexto para enviar ao template
    context = {
        'parts_in_review': user_parts.filter(status='in_review'),
        'parts_approved': user_parts.filter(status='approved'),
        'parts_rejected': user_parts.filter(status='rejected'),
        'projects_in_review': user_projects.filter(status='in_review'),
        'projects_approved': user_projects.filter(status='approved'),
        'projects_rejected': user_projects.filter(status='rejected'),
    }

    return render(request, 'pages/dashboard.html', context)

class StaticPageView(DetailView):
    model = StaticPage
    template_name = "pages/static_page_detail.html"
    context_object_name = "page"
    # Diz à view para buscar a página pelo campo 'slug' na URL, não pelo ID.
    slug_field = 'slug'
    slug_url_kwarg = 'slug'