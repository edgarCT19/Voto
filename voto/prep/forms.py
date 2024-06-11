from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Candidato, Usuario, Acta, PartidoPolitico

class LoginForm(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        }

class RegistrationForm(UserCreationForm):
    rol = forms.ChoiceField(choices=Usuario.ROLES_CHOICES, required=True)  # Agrega campo de rol

    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2', 'rol']  # Añade el campo de rol al formulario
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite la contraseña'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),  # Widget para campo de rol
        }

class ActaForm(forms.ModelForm):
    class Meta:
        model = Acta
        fields = ['fecha', 'casilla', 'pdf', 'votos_partidos', 'votos_candidatos_independientes', 'votos_no_registrados', 'votos_nulos']
        
class PartidoPoliticoForm(forms.ModelForm):
    class Meta:
        model = PartidoPolitico
        fields = ['nombre', 'siglas', 'logo']
        
class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['nombre', 'apellido', 'partido_politico', 'foto_principal', 'foto_secundaria', 'edad']