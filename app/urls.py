#les urls locals de l'application
from django.urls import path

#le module views contient les fonctions qui seront utilisées pour gérer les requêtes HTTP

from . import views

#le chemin d'accès pour chaque fonction dans le module views

urlpatterns = [
    path('', views.home, name='index'),

    #chemin vers inscription
    path('inscription/', views.inscription, name='inscription'),
    #chemin vers dashboard du medecin
    path('medecin/', views.dashboard_medecin, name='dashboard_medecin'),
    #chemin vers les patients
    path('patients/', views.dashboard_patient, name='dashboard_patient'),
    #chemin vers dashboards infirmier
    path('infirmier/', views.dashboard_infirmier, name='dashboard_infirmier'),
    #chemin vers la liste des patients
    path('liste_patient/', views.liste_patients, name='liste_patients'),
    #chemin vers la liste des rendez-vous
    
    #chemin vers la liste des rendez-vous du medecin
    path('medecin/rendezvous/', views.liste_rendezvous_medecin, name='liste_rendezvous_medecin'),


]