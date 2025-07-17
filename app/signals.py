from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ordonnance  # à adapter selon ton nom de modèle
from datetime import timedelta
from django.utils import timezone


@receiver(post_save, sender=Ordonnance)
def generer_prises_medicaments(sender, instance, created, **kwargs):
    if created:
        for medicament in instance.medicaments.all():
            # Supposons que fréquence = "3 fois par jour" et durée = "5 jours"
            try:
                nb_jours = int(''.join(filter(str.isdigit, medicament.duree)))
                nb_par_jour = int(''.join(filter(str.isdigit, medicament.frequence)))
            except ValueError:
                continue  # Sauter si mauvais format

            total_prises = nb_jours * nb_par_jour
            intervalle_heures = 24 / nb_par_jour

            for i in range(total_prises):
                horaire = timezone.now() + timedelta(hours=i * intervalle_heures)
                PriseMedicament.objects.create(
                    medicament=medicament,
                    horaire=horaire,
                    statut='en attente'  # ou False selon ton modèle
                )
