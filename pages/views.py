from django.shortcuts import render

def home_view(request):
    # Por enquanto, vamos apenas renderizar um template simples.
    # No futuro, podemos passar dados como {'nome_usuario': request.user.username}
    return render(request, 'pages/home.html', {})