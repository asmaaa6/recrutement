// Chatbot Script - RecrutAI Platform

(function() {
    'use strict';

    class ChatbotUI {
        constructor() {
            this.chatContainer = document.getElementById('chatContainer');
            this.chatForm = document.getElementById('chatForm');
            this.messageInput = document.getElementById('messageInput');
            this.messages = [];
            this.init();
        }

        init() {
            if (!this.chatForm) return;
            
            this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
            this.messageInput?.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    this.chatForm.dispatchEvent(new Event('submit'));
                }
            });
        }

        handleSubmit(e) {
            e.preventDefault();
            const message = this.messageInput.value.trim();
            
            if (!message) return;
            
            // Ajouter le message utilisateur
            this.addMessage(message, 'user');
            this.messageInput.value = '';
            
            // Simuler la réponse du chatbot
            this.getResponse(message);
        }

        addMessage(text, sender = 'bot') {
            const messageDiv = document.createElement('div');
            messageDiv.className = `d-flex gap-2 mb-3 ${sender === 'user' ? 'justify-content-end' : ''}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'p-3';
            contentDiv.style.borderRadius = '10px';
            contentDiv.style.maxWidth = '70%';
            
            if (sender === 'user') {
                contentDiv.style.background = 'var(--primary)';
                contentDiv.style.color = 'white';
            } else {
                contentDiv.style.background = 'var(--light-blue)';
            }
            
            contentDiv.textContent = text;
            messageDiv.appendChild(contentDiv);
            this.chatContainer.appendChild(messageDiv);
            
            // Scroll vers le bas
            this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
            
            this.messages.push({ text, sender, timestamp: new Date() });
        }

        getResponse(userMessage) {
            // Simuler un délai de réponse
            const typingDiv = document.createElement('div');
            typingDiv.className = 'd-flex gap-2 mb-3';
            typingDiv.innerHTML = '<div class="p-3" style="background: var(--light-blue); border-radius: 10px;"><span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span></div>';
            this.chatContainer.appendChild(typingDiv);
            
            setTimeout(() => {
                // Supprimer l'indicateur de typing
                this.chatContainer.removeChild(typingDiv);
                
                // Obtenir la réponse (en production, appeler une API)
                const response = this.generateResponse(userMessage);
                this.addMessage(response, 'bot');
            }, 1000);
        }

        generateResponse(message) {
            // Base de réponses simple pour la démo
            const responses = {
                'processus': 'Notre processus comprend: 1) Analyse du CV 2) Matching 3) Entretien 4) Décision. Combien de temps cela prend-il?',
                'tempo': 'Le processus de sélection prend généralement 2-4 semaines. Nous vous tiendrons au courant à chaque étape.',
                'competences': 'Les compétences requises varient selon le poste. Consultez l\'offre d\'emploi pour voir les détails spécifiques.',
                'cv': 'Vous pouvez télécharger votre CV dans la section "Upload CV". Nous l\'analyserons automatiquement avec notre IA.',
                'aide': 'Je suis là pour vous aider ! Posez-moi des questions sur le processus de recrutement, les offres d\'emploi, ou votre candidature.',
                'bonjour': 'Bonjour ! Bienvenue sur RecrutAI. Comment puis-je vous aider aujourd\'hui ?',
            };

            const messageLower = message.toLowerCase();
            
            for (const [key, response] of Object.entries(responses)) {
                if (messageLower.includes(key)) {
                    return response;
                }
            }
            
            // Réponse par défaut
            return 'Merci pour votre question! Pour plus d\'informations détaillées, consultez notre FAQ ou contactez notre équipe à info@recrutai.com';
        }

        exportConversation() {
            const csv = this.messages
                .map(msg => `${msg.sender},${msg.timestamp.toISOString()},"${msg.text}"`)
                .join('\n');
            
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'conversation.csv';
            a.click();
        }
    }

    // Initialiser au chargement du DOM
    document.addEventListener('DOMContentLoaded', () => {
        if (document.getElementById('chatContainer')) {
            window.chatbot = new ChatbotUI();
        }
    });

    // Exporter pour usage externe
    window.ChatbotUI = ChatbotUI;
})();
