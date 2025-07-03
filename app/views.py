# Supprimer les imports en double et garder uniquement ceux-ci
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login as auth_login, logout  # Renommer login en auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import User, Service
from app.models import RendezVous 

from .forms import RendezVousForm

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if not user:
            messages.error(request, 'Invalid credentials')
            return render(request, 'conn/login.html', {'error': 'Invalid credentials'})
            
        auth_login(request, user)
        
        if user.is_superuser:
            return redirect('admin')
        
        # Redirect based on user role
        role_redirects = {
            'Médecin': 'dashboard_medecin',
            'Infirmier': 'dashboard_infirmier', 
            'Secrétaire': 'secretaire',
            'Administrateur': 'dashboard_admin'
        }
        
        if user.role in role_redirects:
            return redirect(role_redirects[user.role])
            
        return redirect('home')
        
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
    return render(request, 'medecin/rendezvous/liste.html')

# Vue pour la liste des rendez-vous du médecin
def liste_rendezvous(request):
    return render(request, 'medecin/rendezvoous/rendezvous.html')

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
    personnels = User.objects.all()
    return render(request, 'admin/personnel/liste_personnel.html',{'personnels': personnels})

#vue pour ajout de personnel par l'admin


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PersonnelForm

def ajout_personnel(request):
    
    if request.method == 'POST':
        form = PersonnelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Personnel ajouté avec succès.")
            return redirect('personnel')
        else:
            messages.error(request, "Erreur lors de l’ajout. Vérifiez les champs.")
    else:
        form = PersonnelForm()

    return render(request, 'admin/personnel/ajout_personnel.html', {'form': form})

# vue pour les secretaire

@login_required
def secretaire(request):
    return render(request, 'secretaire/dashboard.html')

#vue pour la liste des rendez-vous du secretaire
def liste_rendezvous_secretaire(request):
    rendezvous_list = RendezVous.objects.all().order_by('-date', '-heure')  # tri du plus récent au plus ancien
    return render(request, 'secretaire/rendezvous/liste.html',{'rendezvous_list': rendezvous_list})

#vue pour la page d'ajout de rendez-vous
def detail_rendezvous(request, id):
    rdv = get_object_or_404(RendezVous, id=id)
    return render(request, 'secretaire/rendezvous/detail.html', {'rdv': rdv})

#vue pour la page de modification de rendez-vous
def supprimer_rendezvous(request, id):
    rdv = get_object_or_404(RendezVous, id=id)

    if request.method == "POST":
        rdv.delete()
        messages.success(request, "Rendez-vous supprimé avec succès.")
        return redirect('liste_rendezvous_secretaire')

    return render(request, 'secretaire/rendezvous/supprimer.html', {'rdv': rdv})

def modifier_rendezvous(request, id):
    rdv = get_object_or_404(RendezVous, id=id)

    if request.method == 'POST':
        form = RendezVousForm(request.POST, instance=rdv)
        if form.is_valid():
            form.save()
            messages.success(request, "Rendez-vous modifié avec succès.")
            return redirect('liste_rendezvous_secretaire')
    else:
        form = RendezVousForm(instance=rdv)

    return render(request, 'secretaire/rendezvous/modifier.html', {'form': form, 'rdv': rdv})

from django.shortcuts import render, redirect, get_object_or_404
from .models import RendezVous, Patient, User
from django.contrib import messages

def ajouter_rendezvous(request):
    if request.method == 'POST':
        patient_nom_prenom = request.POST.get('patient', '').strip()
        medecin_id = request.POST.get('medecin')
        date = request.POST.get('date')
        heure = request.POST.get('heure')
        motif = request.POST.get('motif')
        telephone = request.POST.get('telephone')
        
        try:
            nom, prenom = patient_nom_prenom.split(' ', 1)
            patient_obj = Patient.objects.get(nom=nom, prenom=prenom)
        except (ValueError, Patient.DoesNotExist):
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Patient introuvable'})
            else:
                messages.error(request, "Patient introuvable.")
                return render(request, 'secretaire/rendezvous/ajouter.html')
        
        try:
            medecin_obj = User.objects.get(id=medecin_id, role='Médecin')
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Médecin introuvable'})

        RendezVous.objects.create(
            patient=patient_obj,
            medecin=medecin_obj,
            date=date,
            heure=heure,
            motif=motif,
            telephone=telephone,
            statut='En attente'
        )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            messages.success(request, "Rendez-vous ajouté avec succès.")
            return redirect('liste_rendezvous_secretaire')
    
    # Si GET
    medecins = User.objects.filter(role='Médecin')
    patients = Patient.objects.all()
    return render(request, 'secretaire/rendezvous/ajouter.html', {
        'medecins': medecins,
        'patients': patients,
    })

@login_required
def liste_rv(request):
    user = request.user
    if user.role != 'Médecin':
        return redirect('unauthorized')  # ou autre vue de restriction
    rendezvous = RendezVous.objects.filter(medecin=user).order_by('-date', '-heure')
    return render(request, 'medecin/rendezvoous/liste.html',{'rendezvous': rendezvous})


def dossier_patient_fictif(request, rdv_id):
    # données fictives liées à l'id du rendez-vous
    appointments = [
    {

        "id": 1,
        "patient": "Alice Martin",
        "date": "2025-12-25",
        "heure": "10:00",
        "motif": "Consultation annuelle",
        "statut": "Confirmé",
        "age": 30,
        "antecedents": "Hypertension",
        "allergies": "Pollen",
        "traitements": "Bêtabloquants"
    },
    {
        "id": 2,
        "patient": "Bob Johnson",
        "date": "2026-01-10",
        "heure": "14:30",
        "motif": "Suivi post-opératoire",
        "statut": "En attente",
        "age": 45,
        "antecedents": "Aspergillus",
        "allergies": "Ampoule",
        "traitements": "Antibiotiques"
    }
]

    data = next((a for a in appointments if a["id"] == rdv_id), None)


    if not data:
        return HttpResponse("Rendez-vous non trouvé", status=404)

    return render(request, 'medecin/dossier/dossier.html', {'dossier': data})


