// ============================================
// MAIN JAVASCRIPT - RecrutAI Platform
// ============================================

// Scroll smooth pour les liens d'ancrage
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar transparency on scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = '0 1px 2px rgba(0, 0, 0, 0.05)';
    }
});

// Animation des cartes au scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card, .module-card, .tech-card').forEach(el => {
    observer.observe(el);
});

// Validation des formulaires Bootstrap
(function() {
    'use strict';
    window.addEventListener('load', function() {
        // Récupère les formulaires qui nécessitent une validation
        const forms = document.querySelectorAll('.needs-validation');
        
        Array.from(forms).forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

// Gestion du sombre/clair (optionnelle)
const toggleDarkMode = () => {
    document.documentElement.style.colorScheme = 
        document.documentElement.style.colorScheme === 'dark' ? 'light' : 'dark';
};

// Feedback utilisateur
const showNotification = (message, type = 'info') => {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    const container = document.querySelector('main') || document.body;
    const alertDiv = document.createElement('div');
    alertDiv.innerHTML = alertHTML;
    container.insertBefore(alertDiv.firstElementChild, container.firstChild);
    
    // Auto-dismiss après 5 secondes
    setTimeout(() => {
        const alert = document.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
};

// API Helper
const apiCall = async (endpoint, options = {}) => {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showNotification('Une erreur est survenue. Veuillez réessayer.', 'danger');
        throw error;
    }
};

// Initialisation au chargement
document.addEventListener('DOMContentLoaded', function() {
    console.log('RecrutAI Platform - Application chargée');
    
    // Ajoute des données-attributs pour le tracking
    document.querySelectorAll('[data-track]').forEach(el => {
        el.addEventListener('click', function() {
            const trackName = this.getAttribute('data-track');
            console.log('Event tracked:', trackName);
        });
    });
});

// Format date helper
const formatDate = (date) => {
    return new Date(date).toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

// Format score as percentage
const formatScore = (score) => {
    return Math.round(score * 100) + '%';
};

// Debounce function
const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Export functions for use in other scripts
window.RecrutAI = {
    apiCall,
    showNotification,
    toggleDarkMode,
    formatDate,
    formatScore,
    debounce
};
