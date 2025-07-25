from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date , time, timedelta
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Service(models.Model):
    nom = models.CharField(max_length=250)
    code = models.IntegerField()

    def __str__(self):
        return self.nom

class User(AbstractUser):
    ROLES = (
        ('Médecin', 'Médecin'),
        ('Infirmier', 'Infirmier'),
        ('Secrétaire', 'Secrétaire'),
        ('Administrateur', 'Administrateur'),
        ('Patient', 'Patient'),
        ('Autre', 'Autre'),
    )
    role = models.CharField(max_length=20, choices=ROLES)
    telephone = models.CharField(max_length=20)
    date_creation = models.DateTimeField(auto_now_add=True)

    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='personnels')

  

class Patient(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='dossier_patient'
    )
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)

    groupe_sanguin = models.CharField(
        max_length=3,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-'),
        ],
        null=True, blank=True
    )
    allergies = models.TextField(blank=True, null=True)
    antecedents_medicaux = models.TextField(blank=True, null=True)
    traitements = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    @property
    def get_age(self):
        today = date.today()
        return today.year - self.date_naissance.year - (
            (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
        )






class RendezVous(models.Model):
    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('Confirmé', 'Confirmé'),
        ('Terminé', 'Terminé'),
    ]    
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='rendezvous')
    medecin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                limit_choices_to={'role': 'Médecin'}, related_name='consultations')
    
    date = models.DateField()
    heure = models.TimeField()
    motif = models.TextField()
    telephone = models.CharField(max_length=20)
    statut = models.CharField(max_length=20, choices=[
         ('En attente', 'En attente'),
        ('Confirmé', 'Confirmé'),
        ('Terminé', 'Terminé'),
    ], default='Confirmé')
    
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RDV - {self.patient.nom} {self.patient.prenom} avec Dr. {self.medecin.last_name if self.medecin else 'N/A'} le {self.date} à {self.heure}"


class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    motif = models.TextField()
    diagnostic = models.TextField(blank=True, null=True)
    code_maladie = models.CharField(max_length=50, blank=True, null=True)
    conseils = models.TextField(blank=True, null=True)
    recommandations = models.TextField(blank=True, null=True)
    prochain_rdv = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Consultation de {self.patient} le {self.date.strftime('%d/%m/%Y')}"

class SignesVitaux(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE)
    
    tension_systolique = models.IntegerField(null=True, blank=True)
    tension_diastolique = models.IntegerField(null=True, blank=True)
    frequence_cardiaque = models.IntegerField(null=True, blank=True)
    poids = models.FloatField(null=True, blank=True)
    taille = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    saturation_o2 = models.FloatField(null=True, blank=True)
    glycemie = models.FloatField(null=True, blank=True)

    def imc(self):
        if self.taille and self.poids:
            return round(self.poids / ((self.taille / 100) ** 2), 2)
        return None


class Symptomes(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE)
    
    douleur_thoracique = models.BooleanField(default=False)
    essoufflement = models.BooleanField(default=False)
    palpitations = models.BooleanField(default=False)
    vertiges = models.BooleanField(default=False)
    fatigue = models.BooleanField(default=False)
    oedemes = models.BooleanField(default=False)
    syncope = models.BooleanField(default=False)
    autres = models.TextField(blank=True, null=True)


class AntecedentsMedicaux(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE)

    hypertension = models.BooleanField(default=False)
    diabete = models.BooleanField(default=False)
    hypercholesterolemie = models.BooleanField(default=False)
    infarctus = models.BooleanField(default=False)
    avc = models.BooleanField(default=False)
    fibrillation_auriculaire = models.BooleanField(default=False)
    insuffisance_cardiaque = models.BooleanField(default=False)
    autres = models.TextField(blank=True, null=True)

class AntecedentsFamiliaux(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE)

    maladies_cardiaques = models.TextField(blank=True, null=True)
    deces_precoces = models.TextField(blank=True, null=True)
    autres = models.TextField(blank=True, null=True)

class ModeDeVie(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE)

    fumeur = models.BooleanField(default=False)
    nombre_cigarettes = models.IntegerField(blank=True, null=True)
    ancien_fumeur = models.BooleanField(default=False)
    alcool = models.CharField(max_length=50, choices=[('jamais', 'Jamais'), ('occasionnellement', 'Occasionnellement'), ('souvent', 'Souvent')], default='jamais')
    activite_physique = models.CharField(max_length=50, choices=[('sedentaire', 'Sédentaire'), ('moderee', 'Modérée'), ('active', 'Active')], default='sedentaire')
    alimentation = models.CharField(max_length=50, choices=[('equilibree', 'Équilibrée'), ('deséquilibrée', 'Déséquilibrée')], default='equilibree')
    stress = models.IntegerField(default=5)


class ExamenComplementaire(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    type_examen = models.CharField(max_length=100)
    resultat = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

class Ordonnance(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, related_name='ordonnance')
    date_creation = models.DateTimeField(auto_now_add=True)
    recommandations = models.TextField(blank=True, null=True)
    est_validee = models.BooleanField(default=False)  # ✅ champ ajouté

    def __str__(self):
        return f"Ordonnance - Consultation {self.consultation.id} - {self.consultation.patient}"


class Medicament(models.Model):
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE, related_name='medicaments',  null=True, blank=True)
    nom = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequence = models.CharField(max_length=100)
    duree = models.CharField(max_length=100)

class ConstantesInfirmier(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='constantes')
    date = models.DateField(default=date.today)

    temperature = models.FloatField(null=True, blank=True)
    tension_systolique = models.IntegerField(null=True, blank=True)
    tension_diastolique = models.IntegerField(null=True, blank=True)
    pouls = models.IntegerField(null=True, blank=True)
    poids = models.FloatField(null=True, blank=True)
    taille = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Constantes - {self.patient} - {self.date}"

# models.py

from django.db import models
from django.conf import settings

class Notification(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    est_lu = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.utilisateur.username} - {'Lue' if self.est_lu else 'Non lue'}"


##model pour les taches des infirmiers
# models.py
class Tache(models.Model):
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    medicament = models.CharField(max_length=255)
    dose = models.CharField(max_length=100)
    frequence = models.CharField(max_length=100)
    date_execution = models.DateField()
    heure_execution = models.TimeField(default=time(8, 0))
    est_effectuee = models.BooleanField(default=False)
    
    description = models.TextField(blank=True, null=True)  # ✅ On ajoute ceci

    def __str__(self):
        return f"Tâche {self.medicament} pour {self.patient.nom} le {self.date_execution}"


from datetime import timedelta, time
from django.utils import timezone
from .models import Ordonnance, Tache

@receiver(post_save, sender=Ordonnance)
def generer_taches_infirmier(sender, instance, created, **kwargs):
    patient = instance.consultation.patient

    for medicament in instance.medicaments.all():
        if any(mot in medicament.nom.lower() for mot in ['injection', 'perfus', 'pansement']):
            try:
                duree_jours = int(medicament.duree.split()[0])
            except:
                duree_jours = 1  # Par défaut 1 jour si échec parsing

            for jour in range(duree_jours):
                Tache.objects.create(
                    ordonnance=instance,
                    patient=patient,
                    medicament=medicament.nom,
                    dose=medicament.dosage,
                    frequence=medicament.frequence,
                    date_execution=timezone.now().date() + timedelta(days=jour),
                    heure_execution=time(8, 0)
                )

from django.db import models
from django.utils import timezone
from app.models import Patient  # adapte l'import selon ta structure

class Observation(models.Model):
    TYPE_CHOICES = [
        ('vital', 'Signes vitaux'),
        ('behavior', 'Comportement'),
        ('treatment', 'Réaction au traitement'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="observations")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.patient.nom} - {self.get_type_display()} ({self.date_creation.strftime('%d/%m/%Y %H:%M')})"
