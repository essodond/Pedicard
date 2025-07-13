from django import forms

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Service
from django import forms
from .models import RendezVous, Patient

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

from django import forms

class ConsultationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ConsultationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
    # Informations Patient
    nom = forms.CharField(label="Nom", max_length=100)
    prenom = forms.CharField(label="Prénom", max_length=100)
    sexe = forms.ChoiceField(choices=[('M', 'Masculin'), ('F', 'Féminin')])
    date_naissance = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    telephone = forms.CharField(max_length=20)
    adresse = forms.CharField(required=False)

    # Signes Vitaux
    tension_systolique = forms.CharField(required=False)
    tension_diastolique = forms.CharField(required=False)
    frequence_cardiaque = forms.CharField(required=False)
    poids = forms.CharField(required=False)
    taille = forms.CharField(required=False)
    temperature = forms.CharField(required=False)
    saturation_o2 = forms.CharField(required=False)
    glycemie = forms.CharField(required=False)
    imc = forms.CharField(required=False)

    # Symptômes
    motif_consultation = forms.CharField(widget=forms.Textarea, required=False)
    douleur_thoracique = forms.BooleanField(required=False)
    essoufflement = forms.BooleanField(required=False)
    palpitations = forms.BooleanField(required=False)
    vertiges = forms.BooleanField(required=False)
    fatigue = forms.BooleanField(required=False)
    oedemes = forms.BooleanField(required=False)
    syncope = forms.BooleanField(required=False)
    autres_symptomes = forms.CharField(required=False)

    # Antécédents Médicaux
    hypertension = forms.BooleanField(required=False)
    diabete = forms.BooleanField(required=False)
    hypercholesterolemie = forms.BooleanField(required=False)
    infarctus = forms.BooleanField(required=False)
    avc = forms.BooleanField(required=False)
    fibrillation_auriculaire = forms.BooleanField(required=False)
    insuffisance_cardiaque = forms.BooleanField(required=False)
    autres_antecedents = forms.CharField(required=False)

    # Antécédents Familiaux
    maladies_cardiaques = forms.CharField(required=False)
    deces_precoces = forms.CharField(required=False)
    autres_antecedens_familiaux = forms.CharField(required=False)

    # Mode de vie
    fumeur = forms.BooleanField(required=False)
    nombre_cigarettes = forms.CharField(required=False)
    ancien_fumeur = forms.BooleanField(required=False)
    alcool = forms.ChoiceField(choices=[
        ('jamais', 'Jamais'),
        ('occasionnellement', 'Occasionnellement'),
        ('regulierement', 'Régulièrement')
    ], required=False)
    activite_physique = forms.ChoiceField(choices=[
        ('sedentaire', 'Sédentaire'),
        ('moderee', 'Modérée'),
        ('intense', 'Intense')
    ], required=False)
    alimentation = forms.ChoiceField(choices=[
        ('equilibree', 'Équilibrée'),
        ('desequilibree', 'Déséquilibrée')
    ], required=False)
    stress = forms.IntegerField(min_value=0, max_value=10, required=False)

    # Diagnostic et Suivi
    diagnostic = forms.CharField(widget=forms.Textarea, required=False)
    code_maladie = forms.CharField(required=False)
    conseils = forms.CharField(widget=forms.Textarea, required=False)
    recommandations = forms.CharField(widget=forms.Textarea, required=False)
    prochain_rdv = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)


# forms.py
from django import forms
from .models import Ordonnance, Medicament

class OrdonnanceForm(forms.ModelForm):
    class Meta:
        model = Ordonnance
        fields = ['consultation', 'recommandations']
        widgets = {
            'consultation': forms.Select(attrs={'class': 'form-control'}),
            'recommandations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
class MedicamentForm(forms.ModelForm):
    class Meta:
        model = Medicament
        fields = ['nom', 'dosage', 'frequence', 'duree']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'frequence': forms.TextInput(attrs={'class': 'form-control'}),
            'duree': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [ 'nom', 'prenom', 'date_naissance', 'sexe', 'telephone', 'email', 'adresse', 'groupe_sanguin', 'allergies', 'antecedents_medicaux', 'traitements' ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control rounded-lg shadow-sm border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'placeholder': 'Entrez le nom du patient'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control rounded-lg shadow-sm border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'placeholder': 'Entrez le prénom'
            }),
            'sexe': forms.Select(attrs={
                'class': 'form-select rounded-lg shadow-sm border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500'
            }),
            'date_naissance': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control rounded-lg shadow-sm border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500'
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control rounded-lg shadow-sm border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'placeholder': 'Entrez l\'adresse complète'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control rounded-lg shadow-sm border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'placeholder': '+228 XX XX XX XX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control rounded-lg shadow-sm border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'placeholder': 'exemple@email.com'
            }),
            'groupe_sanguin': forms.Select(attrs={
                'class': 'form-select rounded-lg shadow-sm border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500'
            }),
            'allergies': forms.Textarea(attrs={
                'class': 'form-control rounded-lg shadow-sm border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'rows': 3,
                'placeholder': 'Listez les allergies connues'
            }),
            'antecedents_medicaux': forms.Textarea(attrs={
                'class': 'form-control rounded-lg shadow-sm border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'rows': 3,
                'placeholder': 'Décrivez les antécédents médicaux'
            }),
            'traitements': forms.Textarea(attrs={
                'class': 'form-control rounded-lg shadow-sm border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500',
                'rows': 3,
                'placeholder': 'Listez les traitements en cours'
            })
        }
        labels = {
            'nom': 'Nom du patient',
            'prenom': 'Prénom du patient',
            'sexe': 'Genre',
            'date_naissance': 'Date de naissance',
            'adresse': 'Adresse complète',
            'telephone': 'Numéro de téléphone',
            'email': 'Adresse email',
            'groupe_sanguin': 'Groupe sanguin',
            'allergies': 'Allergies connues',
            'antecedents': 'Antécédents médicaux',
            'traitement_actuel': 'Traitement en cours',
        }
