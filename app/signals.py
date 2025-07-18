# app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ordonnance, Tache
from datetime import timedelta
import time

print("✓ Module signals importé")  # Debug

@receiver(post_save, sender=Ordonnance)
def generer_taches_infirmier(sender, instance, created, **kwargs):
    """Génère automatiquement les tâches infirmières"""
    if created:  # Seulement pour les nouvelles ordonnances
        print(f"⚡ Signal reçu pour Ordonnance #{instance.id}")
        
        patient = instance.consultation.patient
        
        for medicament in instance.medicaments.all():
            if any(mot in medicament.nom.lower() for mot in ['injection', 'perfus', 'pansement']):
                try:
                    duree_jours = int(medicament.duree.split()[0])
                except (ValueError, AttributeError):
                    duree_jours = 1
                
                for jour in range(duree_jours):
                    Tache.objects.create(
                        ordonnance=instance,
                        patient=patient,
                        medicament=medicament.nom,
                        dose=medicament.dosage,
                        frequence=medicament.frequence,
                        date_execution=instance.consultation.date + timedelta(days=jour),
                        heure_execution=time(8, 0)
                    )
                print(f"✓ {duree_jours} tâches créées pour {medicament.nom}")