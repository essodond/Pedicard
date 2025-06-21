from django import forms

class RendezvousForm(forms.Form):
    medecin = forms.CharField(
        label="Nom du médecin",
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Nom complet du médecin'
        })
    )
    patient = forms.CharField(
        label="Nom du patient",
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Nom complet du patient'
        })
    )
    date = forms.DateField(
        label="Date du rendez-vous",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control custom-input'
        })
    )
    time = forms.TimeField(
        label="Heure du rendez-vous",
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control custom-input'
        })
    )
