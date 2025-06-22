# catalog/forms.py

from django import forms
from .models import *

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        # Define os campos que aparecerão no formulário.
        # 'author' e 'status' serão definidos automaticamente na view.
        fields = ['name', 'description', 'category', 'stl_file', 'thumbnail',]

        # (Opcional) Adiciona widgets para customizar a aparência dos campos
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Peça'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descreva a função e dicas de impressão da peça.'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'stl_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

        # (Opcional) Define os rótulos dos campos
        labels = {
            'name': 'Nome da Peça',
            'description': 'Descrição',
            'category': 'Categoria',
            'stl_file': 'Arquivo STL',
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Torna o campo de thumbnail não obrigatório no formulário
            self.fields['thumbnail'].required = False

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        # Incluímos os campos que o usuário deve preencher
        fields = ['title', 'description', 'category', 'parts_used', 'thumbnail',]

        # O campo 'description' usará o CKEditor automaticamente
        # porque o definimos como RichTextUploadingField no models.py.

        # (Opcional) Adiciona widgets e labels para customização
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Projeto'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'parts_used': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '10'}),
        }
        labels = {
            'title': 'Título do Projeto',
            'description': 'Instruções e Detalhes',
            'category': 'Categoria',
            'parts_used': 'Peças Necessárias para este Projeto',
        }