# users/forms.py

from django import forms
from .models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # Campos que o usuário poderá editar em seu perfil
        fields = ['first_name', 'last_name', 'profile_picture']

        # (Opcional) Widgets para estilização com Bootstrap
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'profile_picture': 'Foto de Perfil',
        }