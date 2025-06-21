# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

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