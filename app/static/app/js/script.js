// DOM Elements
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('mainContent');
const sidebarToggle = document.getElementById('sidebarToggle');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileOverlay = document.getElementById('mobileOverlay');
const filterToggle = document.getElementById('filterToggle');
const extendedFilters = document.getElementById('extendedFilters');
const searchInput = document.getElementById('searchInput');
const statusFilter = document.getElementById('statusFilter');
const sortBy = document.getElementById('sortBy');
const doctorFilter = document.getElementById('doctorFilter');
const patientsList = document.getElementById('patientsList');
const emptyState = document.getElementById('emptyState');
const recordsCount = document.getElementById('recordsCount');
const currentDate = document.getElementById('currentDate');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Set current date
    const today = new Date();
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    currentDate.textContent = today.toLocaleDateString('fr-FR', options);
    
    // Initialize filters
    updatePatientsList();
});

// Sidebar Toggle
sidebarToggle.addEventListener('click', function() {
    if (window.innerWidth > 1024) {
        sidebar.style.transform = sidebar.style.transform === 'translateX(-100%)' ? 'translateX(0)' : 'translateX(-100%)';
        mainContent.style.marginLeft = sidebar.style.transform === 'translateX(-100%)' ? '0' : '280px';
    }
});

// Mobile Menu Toggle
mobileMenuBtn.addEventListener('click', function() {
    sidebar.classList.toggle('open');
    mobileOverlay.classList.toggle('show');
});

// Mobile Overlay Click
mobileOverlay.addEventListener('click', function() {
    sidebar.classList.remove('open');
    mobileOverlay.classList.remove('show');
});

// Filter Toggle
filterToggle.addEventListener('click', function() {
    extendedFilters.classList.toggle('show');
    filterToggle.classList.toggle('active');
});

// Search and Filter Event Listeners
searchInput.addEventListener('input', updatePatientsList);
statusFilter.addEventListener('change', updatePatientsList);
sortBy.addEventListener('change', updatePatientsList);
doctorFilter.addEventListener('change', updatePatientsList);

// Update Patients List Function
function updatePatientsList() {
    const searchTerm = searchInput.value.toLowerCase();
    const statusValue = statusFilter.value;
    const sortValue = sortBy.value;
    const doctorValue = doctorFilter.value;
    
    const patientCards = Array.from(patientsList.querySelectorAll('.patient-card'));
    let visibleCards = [];
    
    patientCards.forEach(card => {
        const patientName = card.querySelector('h3').textContent.toLowerCase();
        const contactItems = card.querySelectorAll('.contact-item span');
        const patientStatus = card.getAttribute('data-status');
        const patientDoctor = card.getAttribute('data-doctor');
        
        // Search filter
        let matchesSearch = false;
        if (patientName.includes(searchTerm)) {
            matchesSearch = true;
        } else {
            contactItems.forEach(item => {
                if (item.textContent.toLowerCase().includes(searchTerm)) {
                    matchesSearch = true;
                }
            });
        }
        
        // Status filter
        const matchesStatus = statusValue === 'tous' || patientStatus === statusValue;
        
        // Doctor filter
        const matchesDoctor = doctorValue === 'tous' || patientDoctor === doctorValue;
        
        // Show/hide card
        if (matchesSearch && matchesStatus && matchesDoctor) {
            card.style.display = 'flex';
            visibleCards.push(card);
        } else {
            card.style.display = 'none';
        }
    });
    
    // Sort visible cards
    if (sortValue === 'nom') {
        visibleCards.sort((a, b) => {
            const nameA = a.querySelector('h3').textContent;
            const nameB = b.querySelector('h3').textContent;
            return nameA.localeCompare(nameB);
        });
    } else if (sortValue === 'date') {
        visibleCards.sort((a, b) => {
            const dateA = getLastConsultationDate(a);
            const dateB = getLastConsultationDate(b);
            return new Date(dateB) - new Date(dateA);
        });
    } else if (sortValue === 'consultations') {
        visibleCards.sort((a, b) => {
            const consultationsA = parseInt(a.getAttribute('data-consultations'));
            const consultationsB = parseInt(b.getAttribute('data-consultations'));
            return consultationsB - consultationsA;
        });
    }
    
    // Reorder DOM elements
    visibleCards.forEach(card => {
        patientsList.appendChild(card);
    });
    
    // Update records count
    recordsCount.textContent = `${visibleCards.length} dossier(s) affiché(s)`;
    
    // Show/hide empty state
    if (visibleCards.length === 0) {
        emptyState.style.display = 'block';
        patientsList.style.display = 'none';
    } else {
        emptyState.style.display = 'none';
        patientsList.style.display = 'block';
    }
}

// Helper function to extract last consultation date
function getLastConsultationDate(card) {
    const dateText = card.querySelector('.fa-calendar-check').parentElement.textContent;
    const dateMatch = dateText.match(/(\d{2}\/\d{2}\/\d{4})/);
    if (dateMatch) {
        const [day, month, year] = dateMatch[1].split('/');
        return `${year}-${month}-${day}`;
    }
    return '1970-01-01';
}

// Window Resize Handler
window.addEventListener('resize', function() {
    if (window.innerWidth > 1024) {
        sidebar.classList.remove('open');
        mobileOverlay.classList.remove('show');
        sidebar.style.transform = 'translateX(0)';
        mainContent.style.marginLeft = '280px';
    } else {
        sidebar.style.transform = '';
        mainContent.style.marginLeft = '';
    }
});

// Navigation Active State
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Remove active class from all nav items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Add active class to clicked item
        this.parentElement.classList.add('active');
    });
});

// Button Click Handlers
document.addEventListener('click', function(e) {
    if (e.target.closest('.btn-primary')) {
        const patientName = e.target.closest('.patient-card').querySelector('h3').textContent;
        alert(`Ouverture du dossier médical de ${patientName}`);
    }
    
    if (e.target.closest('.btn-secondary')) {
        const patientName = e.target.closest('.patient-card').querySelector('h3').textContent;
        alert(`Programmation d'une nouvelle consultation pour ${patientName}`);
    }
    
    if (e.target.closest('.btn') && e.target.closest('.header-actions')) {
        alert('Ouverture du formulaire de nouveau patient');
    }
});

// Notification Button
document.querySelector('.notification-btn').addEventListener('click', function() {
    alert('Notifications:\n• Rendez-vous à 14h avec Mme Traore\n• Résultats d\'analyse disponibles\n• Rappel: Réunion équipe médicale à 16h');
});

// Smooth Animations
function addFadeInAnimation() {
    const cards = document.querySelectorAll('.patient-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

// Initialize animations
addFadeInAnimation();

// Search Input Focus Effect
searchInput.addEventListener('focus', function() {
    this.parentElement.style.transform = 'scale(1.02)';
});

searchInput.addEventListener('blur', function() {
    this.parentElement.style.transform = 'scale(1)';
});

// Keyboard Shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        searchInput.focus();
    }
    
    // Escape to clear search
    if (e.key === 'Escape' && document.activeElement === searchInput) {
        searchInput.value = '';
        updatePatientsList();
        searchInput.blur();
    }
});

// Auto-save search preferences
function savePreferences() {
    const preferences = {
        search: searchInput.value,
        status: statusFilter.value,
        sort: sortBy.value,
        doctor: doctorFilter.value
    };
    localStorage.setItem('medicalRecordsPreferences', JSON.stringify(preferences));
}

function loadPreferences() {
    const saved = localStorage.getItem('medicalRecordsPreferences');
    if (saved) {
        const preferences = JSON.parse(saved);
        searchInput.value = preferences.search || '';
        statusFilter.value = preferences.status || 'tous';
        sortBy.value = preferences.sort || 'nom';
        doctorFilter.value = preferences.doctor || 'tous';
        updatePatientsList();
    }
}

// Save preferences on change
[searchInput, statusFilter, sortBy, doctorFilter].forEach(element => {
    element.addEventListener('change', savePreferences);
});

// Load preferences on page load
window.addEventListener('load', loadPreferences);