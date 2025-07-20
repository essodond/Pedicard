from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json
from datetime import datetime
from .models import Patient, Consultation, SignesVitaux, Symptomes, AntecedentsMedicaux , AntecedentsFamiliaux, ModeDeVie, ExamenComplementaire, Medicament
from .models import Patient, Consultation  # Importez vos modèles
from .models import Patient, Consultation, SignesVitaux, Symptomes, AntecedentsMedicaux, AntecedentsFamiliaux, ModeDeVie, ExamenComplementaire, Medicament,Ordonnance,RendezVous



@csrf_exempt
@require_POST
@csrf_exempt
@require_POST
def save_consultation(request, patient_id):
    
    try:
        data = json.loads(request.body)
        print(json.dumps(data, indent=2))  # DEBUG

        medecin_id = data.get('medecin_id')
        symptomes = data.get('symptomes', {})
        motif = symptomes.get('motif_consultation', '')

        if not medecin_id or not motif:
            return JsonResponse({'status': 'error', 'message': 'Champs manquants (medecin_id ou motif_consultation)'}, status=400)

        consultation = Consultation.objects.create(
            patient_id=patient_id,
            medecin_id=medecin_id,
            motif=motif,
            diagnostic=data.get('diagnostic', {}).get('diagnostic', ''),
            code_maladie=data.get('diagnostic', {}).get('code_maladie', ''),
            conseils=data.get('suivi', {}).get('conseils', ''),
            recommandations=data.get('suivi', {}).get('recommandations', ''),
            prochain_rdv=datetime.strptime(data.get('suivi', {}).get('prochain_rdv', ''), '%Y-%m-%d').date() if data.get('suivi', {}).get('prochain_rdv') else None
        )
        # 🔽 AJOUTE CE BLOC ICI 🔽
        rendezvous_id = data.get('rendezvous_id')
        if rendezvous_id:
            try:
                rdv = RendezVous.objects.get(id=rendezvous_id)
                rdv.statut = 'Terminé'
                rdv.save()
            except RendezVous.DoesNotExist:
                pass

        # Signes Vitaux
        signes = data.get('signes_vitaux', {})
        SignesVitaux.objects.create(
            consultation=consultation,
            tension_systolique=signes.get('tension_systolique'),
            tension_diastolique=signes.get('tension_diastolique'),
            frequence_cardiaque=signes.get('frequence_cardiaque'),
            poids=signes.get('poids'),
            taille=signes.get('taille'),
            temperature=signes.get('temperature'),
            saturation_o2=signes.get('saturation_o2'),
            glycemie=signes.get('glycemie')
        )

        # Symptômes
        Symptomes.objects.create(
            consultation=consultation,
            douleur_thoracique=symptomes.get('douleur_thoracique', False),
            essoufflement=symptomes.get('essoufflement', False),
            palpitations=symptomes.get('palpitations', False),
            vertiges=symptomes.get('vertiges', False),
            fatigue=symptomes.get('fatigue', False),
            oedemes=symptomes.get('oedemes', False),
            syncope=symptomes.get('syncope', False),
            autres=symptomes.get('autres_symptomes', '')
        )

        # Antécédents médicaux
        antecedents_medicaux = data.get('antecedents', {}).get('medicaux', {})
        AntecedentsMedicaux.objects.create(
            consultation=consultation,
            hypertension=antecedents_medicaux.get('hypertension', False),
            diabete=antecedents_medicaux.get('diabete', False),
            hypercholesterolemie=antecedents_medicaux.get('hypercholesterolemie', False),
            infarctus=antecedents_medicaux.get('infarctus', False),
            avc=antecedents_medicaux.get('avc', False),
            fibrillation_auriculaire=antecedents_medicaux.get('fibrillation_auriculaire', False),
            insuffisance_cardiaque=antecedents_medicaux.get('insuffisance_cardiaque', False),
            autres=antecedents_medicaux.get('autres', '')
        )

       # Antécédents familiaux
        antecedents_familiaux = data.get('antecedents', {}).get('familiaux', {})
        AntecedentsFamiliaux.objects.create(
            consultation=consultation,
            maladies_cardiaques=antecedents_familiaux.get('maladies_cardiaques', ''),
            deces_precoces=antecedents_familiaux.get('deces_precoces', ''),
            autres=antecedents_familiaux.get('autres', '')
        )


        # Mode de vie
        mode = data.get('mode_vie', {})
        ModeDeVie.objects.create(
            consultation=consultation,
            fumeur=mode.get('fumeur', False),
            nombre_cigarettes=mode.get('nombre_cigarettes') or None,
            ancien_fumeur=mode.get('ancien_fumeur', False),
            alcool=mode.get('alcool', 'jamais'),
            activite_physique=mode.get('activite_physique', 'sedentaire'),
            alimentation=mode.get('alimentation', 'equilibree'),
            stress=mode.get('stress', 5)
        )

        # Examens
        examens = data.get('examens', [])
        for examen in examens:
            ExamenComplementaire.objects.create(
                consultation=consultation,
                type_examen=examen.get('type'),
                date=datetime.strptime(examen.get('date'), '%Y-%m-%d').date(),
                resultat=examen.get('resultat', '')
            )
        
        # Création de l'ordonnance liée à la consultation
        ordonnance = Ordonnance.objects.create(
            consultation=consultation,
            recommandations=data.get('suivi', {}).get('recommandations', '')
        )

        # Médicaments
        medicaments = data.get('traitement', [])
        for med in medicaments:
            Medicament.objects.create(
                ordonnance=ordonnance,
                nom=med.get('nom'),
                dosage=med.get('dose'),
                frequence=med.get('frequence'),
                duree=med.get('duree')
            )

        return JsonResponse({
            'status': 'success', 
            'consultation_id': consultation.id,
            'message': 'Consultation enregistrée',
            'redirect': ''  # Add redirect URL to appointments page
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    



@require_GET
def get_patient_data(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
        return JsonResponse({
            'status': 'success',
            'patient': {
                'id': patient.id,
                'nom': patient.nom,
                'prenom': patient.prenom,
                'date_naissance': patient.date_naissance.strftime('%Y-%m-%d') if patient.date_naissance else None,
                'sexe': patient.sexe,
                'telephone': patient.telephone,
                'adresse': patient.adresse
            }
        })
    except Patient.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'Patient non trouvé'},
            status=404
        )
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': str(e)},
            status=500
        )