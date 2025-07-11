document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    const rdvId = document.body.dataset.rdvId;
    const patientId = document.body.dataset.patientId;
    const medecinId = document.body.dataset.medecinId;

    const storageKey = `consultationData_${rdvId}`;
    const examensKey = `examens_${rdvId}`;
    const medicamentsKey = `medicaments_${rdvId}`;

    let examens = [];
    let medicaments = [];
    let consultationData = {};
    let currentPage = 1;

    function saveData() {
        alert("consultation.js")
        if (!rendezVousId) {
            Swal.fire({
                icon: 'error',
                title: 'Erreur',
                text: "ID du rendez-vous manquant."
            });
            return;
        }
    
        const consultationData = {
            patient_id: patientId,
            medecin_id: medecinId,
            rendezvous_id: rendezVousId,
    
            patientInfo: {
                nom: document.getElementById('nom').value,
                prenom: document.getElementById('prenom').value,
                sexe: document.getElementById('sexe').value,
                dateNaissance: document.getElementById('dateNaissance').value,
                telephone: document.getElementById('telephone').value,
                adresse: document.getElementById('adresse').value
            },
            signesVitaux: {
                tensionSystolique: document.getElementById('tensionSystolique').value,
                tensionDiastolique: document.getElementById('tensionDiastolique').value,
                frequenceCardiaque: document.getElementById('frequenceCardiaque').value,
                poids: document.getElementById('poids').value,
                taille: document.getElementById('taille').value,
                temperature: document.getElementById('temperature').value,
                saturationO2: document.getElementById('saturationO2').value,
                glycemie: document.getElementById('glycemie').value,
                imc: document.getElementById('imc-value').textContent
            },
            symptomes: {
                motifConsultation: document.getElementById('motifConsultation').value,
                douleurThoracique: document.getElementById('douleurThoracique').checked,
                essoufflement: document.getElementById('essoufflement').checked,
                palpitations: document.getElementById('palpitations').checked,
                vertiges: document.getElementById('vertiges').checked,
                fatigue: document.getElementById('fatigue').checked,
                oedemes: document.getElementById('oedemes').checked,
                syncope: document.getElementById('syncope').checked,
                autresSymptomes: document.getElementById('autresSymptomes').value
            },
            antecedentsMedicaux: {
                hypertension: document.getElementById('hypertension').checked,
                diabete: document.getElementById('diabete').checked,
                hypercholesterolemie: document.getElementById('hypercholesterolemie').checked,
                infarctus: document.getElementById('infarctus').checked,
                avc: document.getElementById('avc').checked,
                fibrillationAuriculaire: document.getElementById('fibrillationAuriculaire').checked,
                insuffisanceCardiaque: document.getElementById('insuffisanceCardiaque').checked,
                autres: document.getElementById('autresAntecedents').value
            },
            antecedensFamiliaux: {
                maladiesCardiaques: document.getElementById('maladiesCardiaques').value,
                decesPrecoses: document.getElementById('decesPrecoses').value,
                autres: document.getElementById('autresAntecedensFamiliaux').value
            },
            modeDeVie: {
                fumeur: document.getElementById('fumeur').checked,
                nombreCigarettes: document.getElementById('nombreCigarettes').value,
                ancienFumeur: document.getElementById('ancienFumeur').checked,
                alcool: document.getElementById('alcool').value,
                activitePhysique: document.getElementById('activitePhysique').value,
                alimentation: document.getElementById('alimentation').value,
                stress: document.getElementById('stress').value
            },
            examensComplementaires: examens,
            diagnostic: {
                diagnostic: document.getElementById('diagnostic').value,
                codeMaladie: document.getElementById('codeMaladie').value
            },
            medicaments: medicaments,
            suivi: {
                conseils: document.getElementById('conseils').value,
                recommandations: document.getElementById('recommandations').value,
                prochainRdv: document.getElementById('prochainRdv').value
            }
        };
    
        // Envoi au serveur Django
        fetch(`/app/consultation/sauvegarder/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(consultationData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Succès',
                    text: 'Consultation enregistrée avec succès.'
                });
    
                // Nettoyer localStorage après succès
                localStorage.removeItem('consultationData_' + rendezVousId);
                localStorage.removeItem('examens_' + rendezVousId);
                localStorage.removeItem('medicaments_' + rendezVousId);
                localStorage.removeItem('currentPage_' + rendezVousId);
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Erreur',
                    text: data.message || 'Échec de l\'enregistrement'
                });
            }
        })
        .catch(error => {
            console.error('Erreur :', error);
            Swal.fire({
                icon: 'error',
                title: 'Erreur serveur',
                text: 'Une erreur est survenue.'
            });
        });
    
        // Sauvegarde dans le localStorage (si besoin)
        localStorage.setItem('consultationData_' + rendezVousId, JSON.stringify(consultationData));
        localStorage.setItem('examens_' + rendezVousId, JSON.stringify(examens));
        localStorage.setItem('medicaments_' + rendezVousId, JSON.stringify(medicaments));
        localStorage.setItem('currentPage_' + rendezVousId, currentPage.toString());
    }
    

    function loadSavedData() {
        try {
            const savedData = localStorage.getItem(storageKey);
            const savedExamens = localStorage.getItem(examensKey);
            const savedMedicaments = localStorage.getItem(medicamentsKey);

            if (savedData) {
                consultationData = JSON.parse(savedData);
                populateForm(consultationData);
            }

            if (savedExamens) {
                examens = JSON.parse(savedExamens);
                renderExamens();
            }

            if (savedMedicaments) {
                medicaments = JSON.parse(savedMedicaments);
                renderMedicaments();
            }
        } catch (error) {
            console.error('Erreur chargement localStorage:', error);
        }
    }

    function populateForm(data) {
        if (!data || !data.patientInfo) return;
        document.getElementById('nom').value = data.patientInfo.nom || '';
        document.getElementById('prenom').value = data.patientInfo.prenom || '';
        document.getElementById('sexe').value = data.patientInfo.sexe || '';
        document.getElementById('dateNaissance').value = data.patientInfo.dateNaissance || '';
        document.getElementById('telephone').value = data.patientInfo.telephone || '';
        document.getElementById('adresse').value = data.patientInfo.adresse || '';
        // Tu peux faire pareil pour les autres sections si nécessaire.
    }

    function saveDataLocally() {
        consultationData = {
            patientInfo: {
                nom: document.getElementById('nom').value,
                prenom: document.getElementById('prenom').value,
                sexe: document.getElementById('sexe').value,
                dateNaissance: document.getElementById('dateNaissance').value,
                telephone: document.getElementById('telephone').value,
                adresse: document.getElementById('adresse').value
            },
            // Tu peux ajouter les autres sections ici (signesVitaux, symptomes, etc.)
        };

        localStorage.setItem(storageKey, JSON.stringify(consultationData));
        localStorage.setItem(examensKey, JSON.stringify(examens));
        localStorage.setItem(medicamentsKey, JSON.stringify(medicaments));
    }

    function saveConsultation() {
        saveDataLocally(); // On s'assure que localStorage est à jour

        if (!rdvId || !patientId || !medecinId) {
            alert("Erreur : identifiants manquants.");
            return;
        }

        fetch(`/app/medecin/rendezvous/${rdvId}/consultation/enregistrer/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                rdv_id: rdvId,
                patient_id: patientId,
                medecin_id: medecinId,
                data: consultationData,
                examens: examens,
                medicaments: medicaments
            })
        })
        .then(response => {
            if (response.ok) {
                alert('Consultation sauvegardée avec succès !');
                localStorage.removeItem(storageKey);
                localStorage.removeItem(examensKey);
                localStorage.removeItem(medicamentsKey);
            } else {
                return response.text().then(text => { throw new Error(text); });
            }
        })
        .catch(error => {
            console.error('Erreur sauvegarde:', error);
            alert("Erreur lors de l'enregistrement !");
        });
    }

    // Appels
    loadSavedData();

    // Rends la fonction globale pour pouvoir l’appeler via un bouton dans le template
    window.saveConsultation = saveConsultation;
});
