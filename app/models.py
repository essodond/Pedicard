from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

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

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)

    # Infos médicales
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

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"





class RendezVous(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='rendezvous')
    medecin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                limit_choices_to={'role': 'Médecin'}, related_name='consultations')
    
    date = models.DateField()
    heure = models.TimeField()
    motif = models.TextField()
    telephone = models.CharField(max_length=20)
    statut = models.CharField(max_length=20, choices=[
        ('Confirmé', 'Confirmé'),
        ('Annulé', 'Annulé'),
        ('En attente', 'En attente')
    ], default='En attente')
    
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RDV - {self.patient.nom} {self.patient.prenom} avec Dr. {self.medecin.last_name if self.medecin else 'N/A'} le {self.date} à {self.heure}"
