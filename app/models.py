
from django.db import models
'''
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('Médecin', 'Médecin'),
        ('Infirmier', 'Infirmier'),
        ('Administrateur', 'Administrateur'),
        ('Secrétaire', 'Secrétaire'),
    )
    role = models.CharField(max_length=20, choices=ROLES)
    telephone = models.CharField(max_length=20)
    date_creation = models.DateTimeField(auto_now_add=True)

class Patient(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=10)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    groupe_sanguin = models.CharField(max_length=5)
    date_creation = models.DateTimeField(auto_now_add=True)

class DossierMedical(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    antecedents = models.TextField()
    allergies = models.TextField(blank=True)
    maladies_chroniques = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    derniere_modification = models.DateTimeField(auto_now=True)

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(User, on_delete=models.CASCADE)
    date_consultation = models.DateTimeField()
    motif = models.TextField()
    diagnostic = models.TextField()
    notes = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

class Ordonnance(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateField()
    instructions = models.TextField()

class Medicament(models.Model):
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequence = models.CharField(max_length=100)
    duree = models.CharField(max_length=50)

class RendezVous(models.Model):
    STATUT_CHOICES = (
        ('Programmé', 'Programmé'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
        ('Annulé', 'Annulé'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(User, on_delete=models.CASCADE)
    date_rdv = models.DateTimeField()
    motif = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='Programmé')
    notes = models.TextField(blank=True)

class TacheInfirmier(models.Model):
    PRIORITE_CHOICES = (
        ('Haute', 'Haute'),
        ('Moyenne', 'Moyenne'),
        ('Basse', 'Basse'),
    )
    STATUT_CHOICES = (
        ('À faire', 'À faire'),
        ('En cours', 'En cours'),
        ('Terminée', 'Terminée'),
    )
    infirmier = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.TextField()
    priorite = models.CharField(max_length=20, choices=PRIORITE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='À faire')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_echeance = models.DateTimeField()

class Observation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    personnel = models.ForeignKey(User, on_delete=models.CASCADE)
    date_observation = models.DateTimeField(auto_now_add=True)
    contenu = models.TextField()
    parametres_vitaux = models.TextField(blank=True)
'''