# Supprimer les imports en double et garder uniquement ceux-ci
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout  # Renommer login en auth_login
from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Login attempt: {username}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  # Changé ici : login -> auth_login
            print(f"User authenticated: {user.username}")
            if user.is_superuser:
                return redirect('admin')
            elif user.groups.filter(name='medecin').exists():
                return redirect('dashboard_medecin')
            elif user.groups.filter(name='infirmier').exists():
                return redirect('dashboard_infirmier')
            return redirect('home')
        else:
            print("Authentication failed")
            return render(request, 'conn/login.html', {'error': 'Identifiants invalides'})
            
    return render(request, 'conn/login.html')
# Create your views here.


#vue pour la page d'acceuille

def home(request):
    return render(request, 'index.html')

#vue pour la page le dasboard du medecin

@login_required
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
@login_required
def dashboard_infirmier(request):
    return render(request, 'infirmier/dashboard.html')

#vue pour la page de connection

def login(request):
    return render(request, 'conn/login.html')

#vue pour la page de d'inscription

def inscription(request):
    return render(request, 'conn/inscription.html')


#vue pour le chemin d'accès vers la listes des patients
def liste_patients(request):
    return render(request, 'medecin/liste_patient.html')

def liste_patients_infirmier(request):
    return render(request, 'infirmier/liste_patient_infirmier.html')

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


# vue pour la page des dossiers des infirmiers
def mes_dossiers_infirmier(request):
    return render(request, 'infimier/mes_dossiers_infirmier.html')


# vue pour la page des dossiers des médecins
def mes_dossiers_medecin(request):
    return render(request, 'medecin/mes_dossiers_medecin.html')

# vue pour la page des dossiers des patients
def mes_dossiers_patient(request):
    return render(request, 'patient/mes_dossiers_patient.html')

#vue vers les tache de l'dashboard_infirmier
def taches(request):
    return render(request, 'infirmier/tache.html')

#vue dashboard_admin
@login_required
def dashboard_admin(request):
    return render(request, 'admin/dashboard.html')

#vue pour la page de la liste de personnel pour l'administarateur
def liste_personnel(request):
    return render(request, 'admin/personnel/liste_personnel.html')

#vue pour ajout de personnel par l'admin
def ajout_personnel(request):
    return render(request, 'admin/personnel/ajout_personnel.html')

# vue pour les secretaire
def secretaire(request):
    return render(request, 'secretaire/dashboard.html')