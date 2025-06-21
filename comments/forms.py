# comments/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body'] # O usuário só precisa digitar o corpo do comentário
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Deixe seu comentário...'}),
        }
        labels = {
            'body': '' # Deixamos o rótulo em branco para um design mais limpo
        }