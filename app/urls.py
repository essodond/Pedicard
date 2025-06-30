#les urls locals de l'application
from django.urls import path

#le module views contient les fonctions qui seront utilisées pour gérer les requêtes HTTP

from . import views

#le chemin d'accès pour chaque fonction dans le module views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

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

    path('liste_patient_infirmier/', views.liste_patients_infirmier, name='liste_patients_infirmier'),
    #chemin vers la liste des rendez-vous du patient
    path('patient/rendezvous/', views.liste_rendezvous_patient, name='liste_rendezvous_patient'),
    #chemin vers ledossier du patient
    path('patient/dossier/', views.dossier_patient, name='dossier_patient'),
    #chemin vers la page d'ordonnance du patient
    path('patient/ordonnance/', views.ordonnance_patient, name='ordonnance_patient'),
    
    #chemin vers la liste des rendez-vous du medecin
    path('medecin/', views.rendezvous, name='rendezvous'),
    
    #chemin vers la liste des dossiers de l'infirmier
    path('infirmier/', views.mes_dossiers_infirmier, name='mes_dossiers_infirmier'),
    
    #chemin vers la liste des dossiers du medecin
    path('medecin/dossiers/', views.mes_dossiers_medecin, name='mes_dossiers_medecin'),
    
    #chemin vers la liste des dossiers du patient
    path('patient/', views.mes_dossiers_patient, name='mes_dossiers_patient'),

    #chemin vers les tache de l'infirmier
    path('infirmier/taches/', views.taches, name='taches'),

    #chemin vers le dashboard de l'administrateur
    path('admin/', views.dashboard_admin, name='admin'),

    #chemin vers la liste des personnel
    path('admin/personnel/', views.liste_personnel, name='personnel'),

    #chemin pour l'ajout de personnel
    path('admin/personnel/ajouter/', views.ajout_personnel, name='ajout_personnel'),

    #chemin pour la dashboard du seceretaire
    path('secretaire/', views.secretaire, name='secretaire'),
    #chemin pour la liste des rendez-vous du secretaire
    path('secretaire/rendezvous/', views.liste_rendezvous_secretaire, name='liste_rendezvous_secretaire'),
    #chemin pour l'ajout de rendez-vous
    path('rendezvous/ajouter/', views.ajouter_rendezvous, name='ajouter_rendezvous'),

    #liste des rendez-vous
    path('medecin/rendezvous/', views.liste_rv, name='liste_rendezvous'),



    path('medecin/rendezvous/<int:rdv_id>/', views.dossier_patient_fictif, name='dossier_patient_fictif'),

    


]