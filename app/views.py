# Supprimer les imports en double et garder uniquement ceux-ci
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
from django.contrib.auth import authenticate, login as auth_login, logout  # Renommer login en auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import User, Service
from .forms import ConsultationForm
from django.db.models import Count, Max
from .models import Patient, Consultation, SignesVitaux, Symptomes, ModeDeVie, ExamenComplementaire, Medicament


from app.models import RendezVous 

from .forms import RendezVousForm
from app.models import Patient
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


# Vue pour ajouter une constante par l'infirmier


def ajouter_constantes_infirmier(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)

    if request.method == 'POST':
        ConstantesInfirmier.objects.create(
            patient=patient,
            date=date.today(),
            temperature=request.POST.get('temperature'),
            tension_systolique=request.POST.get('tension_systolique'),
            tension_diastolique=request.POST.get('tension_diastolique'),
            pouls=request.POST.get('pouls'),
            poids=request.POST.get('poids'),
            taille=request.POST.get('taille')
        )
        return redirect('liste_patients_infirmier')  # adapte ce nom si besoin

    return render(request, 'infirmier/ajouter_constante.html', {'patient': patient})


#vue pour la page d'acceuille

def home(request):
    return render(request, 'index.html')

#vue pour la page le dasboard du medecin

@login_required
def dashboard_medecin(request):
    total_patients = Patient.objects.count()
    # Patients actifs = ceux qui ont au moins 1 consultation
    patients_actifs = Patient.objects.annotate(nb_consult=Count('consultation')).filter(nb_consult__gt=0).count()
    total_consultations = Consultation.objects.count()
    # Moyenne consultations par patient actif (évite division par zéro)
    moy_consultations = round(total_consultations / patients_actifs, 2) if patients_actifs > 0 else 0

    context = {
        'total_patients': total_patients,
        'patients_actifs': patients_actifs,
        'total_consultations': total_consultations,
        'moy_consultations': moy_consultations,
    }
    return render(request, 'medecin/dashboard.html', context)
    r

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
    patients = Patient.objects.all()
    today = date.today().strftime('%d/%m/%Y')
    return render(request, 'infirmier/liste_patient_infirmier.html', {
        'patients': patients,
        'today': today
    })

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


from django.db.models import Count, Max, Q
from datetime import date
from .models import Patient
from django.shortcuts import render
from django.db.models import Count, Max, Q
from datetime import date
from .models import Patient

def mes_dossiers_medecin(request):
    
    patients = Patient.objects.all()
    patients_count = patients.count()
    # Recherche
    search = request.GET.get('search', '').strip()

    # Annoter chaque patient avec ses stats
    patients = Patient.objects.annotate(
        nb_consultations=Count('consultation'),
        derniere_consultation=Max('consultation__date')
    )

    # Filtrer par nom (ou prénom si besoin)
    if search:
        patients = patients.filter(Q(nom__icontains=search))

    # Ajouter l'âge à chaque patient
    for p in patients:
        p.age = date.today().year - p.date_naissance.year - (
            (date.today().month, date.today().day) < (p.date_naissance.month, p.date_naissance.day)
        )

    return render(request, 'medecin/dossier/liste.html', {
        'patients': patients,
        'patients_count': patients_count,
    })



#detail dossier
from django.shortcuts import get_object_or_404, render
from datetime import date
from datetime import date

from datetime import date
from django.shortcuts import get_object_or_404, render
from .models import Patient, Consultation, SignesVitaux, Symptomes, ModeDeVie, ExamenComplementaire, Medicament

from django.shortcuts import get_object_or_404, render
from .models import Patient, Consultation, SignesVitaux, Symptomes, ModeDeVie, ExamenComplementaire, Medicament

def detail_dossier(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    consultations = Consultation.objects.filter(patient=patient).order_by('-date')

    consultations_data = []
    for c in consultations:
        try:
            signes = c.signesvitaux
        except SignesVitaux.DoesNotExist:
            signes = None
        try:
            symptomes = c.symptomes
        except Symptomes.DoesNotExist:
            symptomes = None
        try:
            mode_de_vie = c.modedevie
        except ModeDeVie.DoesNotExist:
            mode_de_vie = None

        examens = ExamenComplementaire.objects.filter(consultation=c)
        medicaments = Medicament.objects.filter(consultation=c)

        consultations_data.append({
            'consultation': c,
            'signes': signes,
            'symptomes': symptomes,
            'mode_de_vie': mode_de_vie,
            'examens': examens,
            'medicaments': medicaments,
        })

    # Calcul de l'âge dans la vue (exemple)
    from datetime import date
    age = date.today().year - patient.date_naissance.year - (
        (date.today().month, date.today().day) < (patient.date_naissance.month, patient.date_naissance.day)
    )

    context = {
        'patient': patient,
        'consultations_data': consultations_data,
        'age': age,
    }

    return render(request, 'medecin/dossier/voir.html', context)



    

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


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import RendezVous  # Assure-toi que ce modèle existe

def dossier_patient(request, rdv_id):
    rdv = get_object_or_404(RendezVous, id=rdv_id)
    patient = rdv.patient

    def calcul_age(naissance):
        today = date.today()
        return today.year - naissance.year - (
            (today.month, today.day) < (naissance.month, naissance.day)
        )

    dossier = {
        "id": rdv.id,
        "patient": f"{patient.nom} {patient.prenom}",
        "date": rdv.date,
        "heure": rdv.heure,
        "motif": rdv.motif,
        "statut": rdv.statut,
        "age": calcul_age(patient.date_naissance),
        "antecedents": patient.antecedents_medicaux,
        "allergies": patient.allergies,
        "traitements": getattr(rdv, 'traitement_prescrit', "Aucun"),
    }

    return render(request, 'medecin/dossier/dossier.html', {
        'dossier': dossier,
        'rdv': rdv,
        'patient': patient,
    })


def consultations(request, rdv_id):
    rdv = get_object_or_404(RendezVous, id=rdv_id)
    patient = rdv.patient  # supposant que RendezVous a un champ ForeignKey vers Patient

    return render(request, 'medecin/consultation/index.html', {
        'rdv': rdv,
        'patient': patient,
    })
    

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import *

@csrf_exempt
def enregistrer_consultation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Création d'une Consultation
            patient_id = data.get('patient_id')  # Assure-toi d'envoyer l'ID du patient
            medecin_id = data.get('medecin_id')  # Même chose pour le médecin

            patient = Patient.objects.get(id=patient_id)
            medecin = User.objects.get(id=medecin_id)

            consultation = Consultation.objects.create(
                patient=patient,
                medecin=medecin,
                motif=data['symptomes']['motifConsultation'],
                diagnostic=data['diagnostic']['diagnostic'],
                code_maladie=data['diagnostic']['codeMaladie'],
                conseils=data['suivi']['conseils'],
                recommandations=data['suivi']['recommandations'],
                prochain_rdv=data['suivi']['prochainRdv'] or None,
            )

            # Signes Vitaux
            SignesVitaux.objects.create(
                consultation=consultation,
                tension_systolique=data['signesVitaux']['tensionSystolique'],
                tension_diastolique=data['signesVitaux']['tensionDiastolique'],
                frequence_cardiaque=data['signesVitaux']['frequenceCardiaque'],
                poids=data['signesVitaux']['poids'],
                taille=data['signesVitaux']['taille'],
                temperature=data['signesVitaux']['temperature'],
                saturation_o2=data['signesVitaux']['saturationO2'],
                glycemie=data['signesVitaux']['glycemie'],
            )

            # Symptômes
            Symptomes.objects.create(
                consultation=consultation,
                douleur_thoracique=data['symptomes']['douleurThoracique'],
                essoufflement=data['symptomes']['essoufflement'],
                palpitations=data['symptomes']['palpitations'],
                vertiges=data['symptomes']['vertiges'],
                fatigue=data['symptomes']['fatigue'],
                oedemes=data['symptomes']['oedemes'],
                syncope=data['symptomes']['syncope'],
                autres=data['symptomes']['autresSymptomes'],
            )

            # Antécédents médicaux
            AntecedentsMedicaux.objects.create(
                consultation=consultation,
                hypertension=data['antecedentsMedicaux']['hypertension'],
                diabete=data['antecedentsMedicaux']['diabete'],
                hypercholesterolemie=data['antecedentsMedicaux']['hypercholesterolemie'],
                infarctus=data['antecedentsMedicaux']['infarctus'],
                avc=data['antecedentsMedicaux']['avc'],
                fibrillation_auriculaire=data['antecedentsMedicaux']['fibrillationAuriculaire'],
                insuffisance_cardiaque=data['antecedentsMedicaux']['insuffisanceCardiaque'],
                autres=data['antecedentsMedicaux']['autres'],
            )

            # Médicaments
            for med in data['medicaments']:
                Medicament.objects.create(
                    consultation=consultation,
                    nom=med['nom'],
                    dosage=med['dosage'],
                    frequence=med['frequence'],
                    duree=med['duree'],
                )

            # Examens
            for ex in data['examensComplementaires']:
                ExamenComplementaire.objects.create(
                    consultation=consultation,
                    type_examen=ex['type'],
                    resultat=ex.get('resultat', '')
                )

            return JsonResponse({'success': True, 'message': "Consultation enregistrée avec succès."})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt  # si tu n’envoies pas encore CSRF correctement
def sauvegarder_consultation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Consultation reçue :", data)

            # Ici tu peux stocker en base : créer une Consultation(), etc.

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from datetime import datetime
from .models import (
    Consultation, SignesVitaux, Symptomes, 
    AntecedentsMedicaux, AntecedentsFamiliaux,
    ModeDeVie, ExamenComplementaire, Medicament
)

@csrf_exempt
@require_POST
def save_consultation(request):
    try:
        data = json.loads(request.body)
        
        # Création de la consultation de base
        consultation = Consultation.objects.create(
            patient=request.user.patient_profile,  # À adapter selon votre modèle
            medecin=request.user,
            motif=data.get('motifConsultation', ''),
            diagnostic=data.get('diagnostic', ''),
            code_maladie=data.get('codeMaladie', ''),
            conseils=data.get('conseils', ''),
            recommandations=data.get('recommandations', ''),
            prochain_rdv=datetime.strptime(data.get('prochainRdv', ''), '%Y-%m-%d').date() if data.get('prochainRdv') else None
        )
        
        # Signes vitaux
        signes_vitaux = data.get('signesVitaux', {})
        SignesVitaux.objects.create(
            consultation=consultation,
            tension_systolique=signes_vitaux.get('tensionSystolique'),
            tension_diastolique=signes_vitaux.get('tensionDiastolique'),
            frequence_cardiaque=signes_vitaux.get('frequenceCardiaque'),
            poids=signes_vitaux.get('poids'),
            taille=signes_vitaux.get('taille'),
            temperature=signes_vitaux.get('temperature'),
            saturation_o2=signes_vitaux.get('saturationO2'),
            glycemie=signes_vitaux.get('glycemie')
        )
        
        # Symptômes
        symptomes = data.get('symptomes', {})
        Symptomes.objects.create(
            consultation=consultation,
            douleur_thoracique=symptomes.get('douleurThoracique', False),
            essoufflement=symptomes.get('essoufflement', False),
            palpitations=symptomes.get('palpitations', False),
            vertiges=symptomes.get('vertiges', False),
            fatigue=symptomes.get('fatigue', False),
            oedemes=symptomes.get('oedemes', False),
            syncope=symptomes.get('syncope', False),
            autres=symptomes.get('autresSymptomes', '')
        )
        # Antécédents médicaux
        antecedents_medicaux = data.get('antecedentsMedicaux', {})
        AntecedentsMedicaux.objects.create(
            consultation=consultation,
            hypertension=antecedents_medicaux.get('hypertension', False),
            diabete=antecedents_medicaux.get('diabete', False),
            hypercholesterolemie=antecedents_medicaux.get('hypercholesterolemie', False),
            infarctus=antecedents_medicaux.get('infarctus', False),
            avc=antecedents_medicaux.get('avc', False),
            fibrillation_auriculaire=antecedents_medicaux.get('fibrillationAuriculaire', False),
            insuffisance_cardiaque=antecedents_medicaux.get('insuffisanceCardiaque', False),
            autres=antecedents_medicaux.get('autres', '')   
        )
        
        # Continuez avec les autres modèles (AntecedentsMedicaux, etc.)
        
        return JsonResponse({'status': 'success', 'consultation_id': consultation.id})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
def consultation_view(request, rdv_id):
    
    rdv = get_object_or_404(RendezVous, id=rdv_id)
    patient = rdv.patient  # supposant que RendezVous a un FK vers Patient

    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            # Traitement ici
            print(form.cleaned_data)
            return redirect('dashboard_medecin')
    else:
        form = ConsultationForm(initial={
            'nom': patient.nom,
            'prenom': patient.prenom,
            'sexe': patient.sexe,
            'date_naissance': patient.date_naissance,
            'telephone': patient.telephone,
            'adresse': patient.adresse,
        })

    return render(request, 'medecin/consultation/index.html', {
        'form': form,
        'patient': patient,
        'rdv': rdv,
    })


def consultation_form(request):
    patient_id = request.GET.get('patient_id')
    rdv_id = request.GET.get('rdv_id')
    
    if not patient_id:
        return redirect('liste_rdv')
    
    try:
        patient = Patient.objects.get(id=patient_id)
        rdv = RendezVous.objects.get(id=rdv_id) if rdv_id else None
        return render(request, 'consultation_form.html', {
            'patient': patient,
            'rdv': rdv
        })
    except (Patient.DoesNotExist, RendezVous.DoesNotExist):
        return redirect('liste_rdv')


# views.py
from django.shortcuts import get_object_or_404, render
from .models import Ordonnance



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Ordonnance


from django.core.paginator import Paginator

@login_required
def liste_ordonnances_medecin(request):
    medecin = request.user

    ordonnances_all = (
        Ordonnance.objects
        .filter(consultation__medecin=medecin)
        .select_related('consultation__patient')
        .prefetch_related('medicaments')
        .order_by('-date_creation')
    )

    paginator = Paginator(ordonnances_all, 5)  # 5 ordonnances par page
    page_number = request.GET.get('page')
    ordonnances = paginator.get_page(page_number)

    context = {
        'ordonnances': ordonnances,
        'total': ordonnances_all.count(),
        'actives': ordonnances_all.filter(recommandations__isnull=False).exclude(recommandations='').count(),
        'completes': ordonnances_all.filter(recommandations='').count(),
        'attente': ordonnances_all.filter(recommandations__isnull=True).count(),
    }
    return render(request, 'medecin/ordonnance/liste.html', context)



# views.py
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from .models import Consultation, Ordonnance, Medicament
from .forms import OrdonnanceForm, MedicamentForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Consultation, Ordonnance, Medicament
from django.contrib import messages
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Ordonnance, Consultation, Medicament, Patient
from .forms import OrdonnanceForm, MedicamentForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import OrdonnanceForm
from .models import Ordonnance, Medicament, Patient, Consultation

def ajouter_ordonnance(request):
    patients = Patient.objects.all()
    last_consultation = Consultation.objects.filter(medecin=request.user).order_by('-date').first()

    if request.method == 'POST':
        consultation_id = request.POST.get('consultation')
        consultation = get_object_or_404(Consultation, id=consultation_id)

        # 🛑 Vérifie s'il existe déjà une ordonnance pour cette consultation
        if hasattr(consultation, 'ordonnance'):
            messages.error(request, "Une ordonnance existe déjà pour cette consultation.")
            return redirect('liste_ordonnances_medecin')

        # 💾 Crée l’ordonnance avec le formulaire
        ordonnance_form = OrdonnanceForm(request.POST)
        if ordonnance_form.is_valid():
            ordonnance = ordonnance_form.save(commit=False)
            ordonnance.consultation = consultation
            ordonnance.save()

            # 🔁 Récupère les listes des médicaments
            noms = request.POST.getlist('medications[]')
            dosages = request.POST.getlist('dosages[]')
            frequences = request.POST.getlist('frequence[]')
            durees = request.POST.getlist('durations[]')

            # 💊 Ajoute les médicaments à l'ordonnance
            for nom, dosage, frequence, duree in zip(noms, dosages, frequences, durees):
                Medicament.objects.create(
                    ordonnance=ordonnance,
                    nom=nom,
                    dosage=dosage,
                    frequence=frequence,
                    duree=duree
                )

            messages.success(request, "Ordonnance créée avec succès.")
            return redirect('liste_ordonnances')
        else:
            messages.error(request, "Formulaire invalide.")

    context = {
        'patients': patients,
        'last_consultation': last_consultation,
    }
    return render(request, 'medecin/ordonnance/ajouter.html', context)


def voir_ordonnance(request, consultation_id):
    ordonnance = get_object_or_404(Ordonnance, consultation__id=consultation_id)
    medicaments = ordonnance.medicaments.all()
    return render(request, 'ordonnances/detail.html', {
        'ordonnance': ordonnance,
        'medicaments': medicaments,
    })
    
    