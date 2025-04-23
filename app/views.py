from django.shortcuts import render


# Create your views here.
#vue pour la page d'acceuille

def home(request):
    return render(request, 'index.html')

#vue pour la page le dasboard du medecin

def dashboard_medecin(request):
    return render(request, 'medecin/dashboard.html')

#vue pour la page des patients

def dashboard_patient(request):
    return render(request, 'patient/dashboard.html')

#vue pour la page des consultations

def consultations(request):
    return render(request, 'consultations.html')

#vue pour la page des prescriptions

def prescriptions(request):
    return render(request, 'prescriptions.html')

#vue pour la page des rendez-vous

def rendezvous(request):
    return render(request, 'rendezvous.html')

#vue pour la page des parametres

def parametres(request):
    return render(request, 'parametres.html')

#vue pour la page des infirmiers

def dashboard_infirmier(request):
    return render(request, 'infirmier/dashboard.html')

#vue pour la page de connection

def connection(request):
    return render(request, 'connection.html')

#vue pour la page de d'inscription

def inscription(request):
    return render(request, 'conn/inscription.html')


#vue pour le chemin d'accès vers la listes des patients
def liste_patients(request):
    return render(request, 'medecin/liste_patient.html')

# Vue pour la page des rendez-vous généraux
def rendezvous(request):
    return render(request, 'rendezvous.html')

# Vue pour la liste des rendez-vous du médecin
def liste_rendezvous_medecin(request):
    return render(request, 'medecin/rendezvous.html')

# Vue pour la liste des rendez-vous du patient
def liste_rendezvous_patient(request):
    return render(request,'patient/rdv.html')

#vue pour le dossier de patient
def dossier_patient(request):
    return render(request,'patient/dossier.html')

#vue vers la page d'ordonnance du patient
def ordonnance_patient(request):
    return render(request,'patient/ordonnance.html')


