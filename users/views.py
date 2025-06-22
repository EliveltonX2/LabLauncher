# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import CustomUser
from catalog.models import Part, Project

@login_required
def profile_update_view(request):
    # Usamos um if para separar a lógica de quando o usuário envia o formulário (POST)
    # e de quando ele apenas visita a página (GET).
    if request.method == 'POST':
        # Cria uma instância do formulário com os dados enviados (request.POST)
        # e os arquivos enviados (request.FILES), associada ao usuário atual (instance=request.user).
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('profile') # Redireciona de volta para a mesma página
    else:
        # Se for uma visita normal (GET), apenas mostra o formulário preenchido
        # com os dados atuais do usuário.
        form = ProfileForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'users/profile.html', context)

def public_profile_view(request, username):
    # Busca o usuário pelo username na URL, ou retorna erro 404 se não existir
    profile_user = get_object_or_404(CustomUser, username=username)

    # Busca as contribuições APROVADAS deste usuário
    approved_parts = Part.objects.filter(author=profile_user, status='approved')
    approved_projects = Project.objects.filter(author=profile_user, status='approved')

    # Calcula as estatísticas
    context = {
        'profile_user': profile_user,
        'approved_parts': approved_parts,
        'approved_projects': approved_projects,
        'parts_count': approved_parts.count(),
        'projects_count': approved_projects.count(),
    }
    return render(request, 'users/public_profile.html', context)