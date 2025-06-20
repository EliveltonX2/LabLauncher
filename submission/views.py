# submission/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from catalog.models import Part, Project

def is_curator(user):
    """
    Verifica se o usuário é um curador (membro da staff).
    """
    return user.is_authenticated and user.is_staff

@user_passes_test(is_curator) # Protege a view, só permite acesso a curadores
def curation_queue_view(request):
    """
    Busca todas as peças e projetos que estão aguardando revisão.
    """
    pending_parts = Part.objects.filter(status='in_review').order_by('created_at')
    pending_projects = Project.objects.filter(status='in_review').order_by('created_at')

    context = {
        'pending_parts': pending_parts,
        'pending_projects': pending_projects,
    }

    return render(request, 'submission/curation_queue.html', context)