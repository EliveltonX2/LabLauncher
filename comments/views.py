# Create your views here.
# comments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm

@login_required
def add_comment_view(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, pk=content_type_id)
    obj = content_type.get_object_for_this_type(pk=object_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.content_object = obj
            new_comment.save()

    # Redireciona de volta para a página do objeto (seja peça ou projeto)
    return redirect(obj.get_absolute_url()) if hasattr(obj, 'get_absolute_url') else '/'