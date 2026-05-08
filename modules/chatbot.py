# Module Chatbot
# Assistant conversationnel assisté par IA

from datetime import datetime

class RecruitmentChatbot:
    """Chatbot pour assister les candidats"""
    
    def __init__(self):
        # Base de réponses simples
        self.responses = {
            'hello': [
                "Bonjour! Je suis l'assistant RecrutAI. Comment puis-je vous aider?",
                "Bienvenue! Que puis-je faire pour vous?",
            ],
            'process': [
                "Notre processus de recrutement comprend: 1) Analyse du CV 2) Matching avec offres 3) Entretien 4) Décision",
                "Le processus typique prend 2-4 semaines.",
            ],
            'skills': [
                "Les compétences principales recherchées varient selon le poste.",
                "Consultez l'offre d'emploi pour voir les compétences requises.",
            ],
            'timeline': [
                "Vous devriez recevoir une réponse dans les 2 semaines.",
                "Notre équipe examinera votre candidature rapidement.",
            ],
            'contact': [
                "Vous pouvez nous contacter à: info@recrutai.com",
                "Téléphone: +33 1 23 45 67 89",
            ]
        }
    
    def get_response(self, user_message):
        """
        Génère une réponse à partir du message utilisateur
        
        Args:
            user_message: Message de l'utilisateur
        
        Returns:
            str: Réponse du chatbot
        """
        
        message_lower = user_message.lower()
        
        # Keywords pour chaque catégorie
        if any(word in message_lower for word in ['bonjour', 'salut', 'hello', 'hi']):
            return self._random_response('hello')
        
        elif any(word in message_lower for word in ['processus', 'étapes', 'comment ça marche']):
            return self._random_response('process')
        
        elif any(word in message_lower for word in ['compétences', 'skills', 'requis']):
            return self._random_response('skills')
        
        elif any(word in message_lower for word in ['combien de temps', 'timeline', 'réponse']):
            return self._random_response('timeline')
        
        elif any(word in message_lower for word in ['contact', 'téléphone', 'email']):
            return self._random_response('contact')
        
        else:
            return "Merci pour votre question. Pour plus d'informations, consultez notre FAQ ou contactez notre équipe."
    
    def _random_response(self, category):
        """Retourne une réponse aléatoire d'une catégorie"""
        import random
        if category in self.responses:
            return random.choice(self.responses[category])
        return "Je n'ai pas trouvé de réponse à votre question."
    
    def store_conversation(self, user_id, message, response):
        """Stocke la conversation dans la base de données"""
        # À implémenter
        pass

class AdvancedChatbot(RecruitmentChatbot):
    """Chatbot avancé avec ML (optional)"""
    
    def __init__(self):
        super().__init__()
        self.model = None  # Modèle NLP avancé à charger
    
    def analyze_sentiment(self, message):
        """Analyse le sentiment du message"""
        # À implémenter avec TextBlob ou transformers
        pass

# Instance globale
chatbot = RecruitmentChatbot()
