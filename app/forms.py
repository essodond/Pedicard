from django import forms

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Service
from django import forms
from .models import RendezVous

class PersonnelForm(forms.ModelForm):
    mot_de_passe = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le mot de passe'})
    )

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'role', 'service', 'email', 'telephone']
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom',
        }
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le prénom'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@email.com'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: +228 XX XX XX XX'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # email comme username
        user.set_password(self.cleaned_data['mot_de_passe'])  # hash mot de passe
        user.is_staff = True  # Pour qu'il puisse accéder au panel admin s'il est autorisé
        if commit:
            user.save()
        return user


class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['patient', 'medecin', 'date', 'heure', 'motif', 'telephone', 'statut']
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'form-control custom-input',
            }),
            'medecin': forms.Select(attrs={
                'class': 'form-control custom-input',
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control custom-input',
            }),
            'heure': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control custom-input',
            }),
            'motif': forms.Textarea(attrs={
                'class': 'form-control custom-input',
                'rows': 3,
                'placeholder': 'Motif de la consultation'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Numéro du patient'
            }),
            'statut': forms.Select(attrs={
                'class': 'form-control custom-input',
            }),
        }