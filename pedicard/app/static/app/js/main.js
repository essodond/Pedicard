// Éléments DOM
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');

// Animation des cartes de fonctionnalités
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.slide-in').forEach(element => {
    observer.observe(element);
});

// Gestion des modales avec animations
function showModal(modal) {
    modal.classList.remove('hidden');
    requestAnimationFrame(() => {
        modal.classList.add('visible');
    });
}

function hideModal(modal) {
    modal.classList.remove('visible');
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 300);
}

// Gestionnaires d'événements pour les boutons
[...document.querySelectorAll('#showLoginBtn')].forEach(btn => {
    btn.addEventListener('click', () => showModal(loginForm));
});

[...document.querySelectorAll('#showRegisterBtn, #showRegisterBtn2')].forEach(btn => {
    btn.addEventListener('click', () => showModal(registerForm));
});

// Fermeture des modales
document.querySelectorAll('.close-modal').forEach(button => {
    button.addEventListener('click', () => {
        hideModal(loginForm);
        hideModal(registerForm);
    });
});

// Fermeture des modales en cliquant en dehors
[loginForm, registerForm].forEach(modal => {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            hideModal(modal);
        }
    });
});

// Gestion des soumissions de formulaires
document.getElementById('loginFormElement').addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const loginData = {
        email: formData.get('email'),
        password: formData.get('password')
    };
    console.log('Tentative de connexion:', loginData);
    hideModal(loginForm);
});

document.getElementById('registerFormElement').addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const registerData = {
        nom: formData.get('nom'),
        prenom: formData.get('prenom'),
        email: formData.get('email'),
        password: formData.get('password')
    };
    console.log('Tentative d\'inscription:', registerData);
    hideModal(registerForm);
});