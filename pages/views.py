# pages/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from catalog.models import Part, Project
from .models import StaticPage
from django.views.generic import DetailView
from catalog.models import Part, Project 

def home_view(request):
    # Busca os 3 projetos mais recentes marcados como destaque
    featured_projects = Project.objects.filter(is_hall_of_fame=True, status='approved').order_by('-created_at')[:3]

    # Busca as 4 peças mais recentes marcadas como destaque
    featured_parts = Part.objects.filter(is_hall_of_fame=True, status='approved').order_by('-created_at')[:4]

    context = {
        'featured_projects': featured_projects,
        'featured_parts': featured_parts,
    }
    return render(request, 'pages/home.html', context)

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
        'parts_approved_count': user_parts.filter(status='approved').count(),
        'parts_rejected': user_parts.filter(status='rejected'),
        'projects_in_review': user_projects.filter(status='in_review'),
        'projects_approved': user_projects.filter(status='approved'),
        'projects_approved_count': user_projects.filter(status='approved').count(),
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

# pages/views.py
def hall_of_fame_view(request):
    featured_parts = Part.objects.filter(is_hall_of_fame=True, status='approved')
    featured_projects = Project.objects.filter(is_hall_of_fame=True, status='approved')

    context = {
        'featured_parts': featured_parts,
        'featured_projects': featured_projects,
    }
    return render(request, 'pages/hall_of_fame.html', context)