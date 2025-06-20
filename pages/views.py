# pages/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required # Para proteger a view
from catalog.models import Part, Project # Para buscar os dados

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