#les urls locals de l'application
from django.urls import path

#le module views contient les fonctions qui seront utilisées pour gérer les requêtes HTTP

from . import views
from . import api_views

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

    path('dossier/<int:patient_id>/', views.detail_dossier, name='detail_dossier'),
    
    #chemin vers la liste des dossiers du patient
    path('patient/', views.mes_dossiers_patient, name='mes_dossiers_patient'),

    

    #chemin vers le dashboard de l'administrateur
    path('admin/', views.dashboard_admin, name='admin'),

    #chemin vers la liste des personnel
    path('admin/personnel/', views.liste_personnel, name='personnel'),

    #chemin pour l'ajout de personnel
    path('admin/personnel/ajouter/', views.ajout_personnel, name='ajout_personnel'),

    #chemin pour la dashboard du seceretaire
    path('secretaire/', views.secretaire, name='secretaire'),

    #chemin pour la liste des patients
    path('secretaire/patients/', views.liste_patients_secretaire, name='liste_patients_secretaire'),
    #chemin pour la liste des rendez-vous du secretaire
    path('secretaire/rendezvous/', views.liste_rendezvous_secretaire, name='liste_rendezvous_secretaire'),
    path('rendezvous/<int:id>/', views.detail_rendezvous, name='detail_rendezvous'),
    path('rendezvous/<int:id>/supprimer/', views.supprimer_rendezvous, name='supprimer_rendezvous'),
    path('rendezvous/<int:id>/modifier/', views.modifier_rendezvous, name='modifier_rendezvous'),


    #chemin pour l'ajout de rendez-vous
    path('rendezvous/ajouter/', views.ajouter_rendezvous, name='ajouter_rendezvous'),

    #liste des rendez-vous
    path('medecin/rendezvous/', views.liste_rv, name='liste_rendezvous'),



    path('medecin/rendezvous/<int:rdv_id>/dossier/', views.dossier_patient, name='dossier_patient'),

    #vue pour la consultation
    #path('medecin/rendezvous/<int:rdv_id>/consultation/', views.consultations, name='consultation'),
    # urls.py
    path('medecin/rendezvous/<int:rdv_id>/consultation/', views.consultation_view, name='consultation_view'),





    path('mes-ordonnances/', views.liste_ordonnances_medecin, name='liste_ordonnances_medecin'),
    path('consultation/ajouter-ordonnance/', views.ajouter_ordonnance, name='ajouter_ordonnance'),
    path('ordonnances/<int:ordonnance_id>/', views.detail_ordonnance, name='detail_ordonnance'),
    path('ordonnances/<int:ordonnance_id>/pdf/', views.telecharger_ordonnance_pdf, name='telecharger_ordonnance_pdf'),





    path('api/consultations/<int:patient_id>/', api_views.save_consultation, name='save_consultation_api'),
    path('api/patients/<int:patient_id>/', api_views.get_patient_data, name='get_patient_api'),

   # urls.py
    path('medecin/rendezvous/<int:patient_id>/consultation/', views.consultation_view, name='consultation_view'),

    
    #chemin pour ajouter une constante
    path('patients/<int:patient_id>/constantes/ajouter/', views.ajouter_constantes_infirmier, name='ajouter_constantes_infirmier'),
    
    #chemin pour afficher les constantes d'un patient
    path('patients/<int:patient_id>/constantes/', views.constantes_patient, name='constantes_patient'),
    
    #chemin pour afficher ajouter un patient 
    path('secretaire/ajouter/', views.ajouter_patient, name='ajouter_patient'),
    path('notifications/marquer_tout_lu/', views.marquer_tout_lu, name='marquer_tout_lu'),

    path('admin/statistic/', views.statistics, name='statistic'),
    #chemin pour les taches de l'infirmier

    path('infirmier/taches/', views.liste_taches, name='liste_taches'),
    path('infirmier/observation/', views.observation, name='observation'),
    path('infirmier/planing/', views.planing, name='planing'),
    path('infirmier/taches-json/', views.taches_json, name='taches_json'),
    path('infirmier/ajouter-tache/', views.ajouter_tache_manuellement, name='ajouter_tache'),
    path('tache/<int:pk>/terminer/', views.terminer_tache, name='terminer_tache'),

    path('admin/statistiques/', views.admin_stats, name='admin_stats'),

    
    






]