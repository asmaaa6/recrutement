# Module Chatbot - Powered by Claude AI
import os
import anthropic

class RecruitmentChatbot:
    """Chatbot intelligent pour RecrutAI"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get('ANTHROPIC_API_KEY')
        )
        self.conversation_history = []
    
    def get_response(self, user_message):
        """Génère une réponse intelligente via Claude"""
        try:
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system="""Tu es l'assistant virtuel de RecrutAI, 
                une plateforme de recrutement intelligente algérienne.
                Tu aides les candidats et recruteurs en français.
                Tu es professionnel, sympathique et concis.
                Tu réponds uniquement aux questions liées au recrutement,
                aux offres d'emploi, aux CV et à la plateforme RecrutAI.""",
                messages=self.conversation_history
            )
            
            response = message.content[0].text
            
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Garder seulement les 10 derniers messages
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return response
            
        except Exception as e:
            print(f"Erreur chatbot: {e}")
            return self._fallback_response(user_message)
    
    def _fallback_response(self, message):
        """Réponse basique sans API"""
        message_lower = message.lower()
        
        if any(w in message_lower for w in ['bonjour', 'salut', 'hello']):
            return "Bonjour! Je suis l'assistant RecrutAI. Comment puis-je vous aider?"
        
        elif any(w in message_lower for w in ['offre', 'emploi', 'poste']):
            return "Consultez nos offres d'emploi dans la section Offres. Vous pouvez filtrer par domaine et localisation."
        
        elif any(w in message_lower for w in ['cv', 'candidature']):
            return "Pour soumettre votre CV, allez dans votre espace candidat et cliquez sur Upload CV."
        
        elif any(w in message_lower for w in ['score', 'matching', 'compatibilité']):
            return "Notre système analyse votre CV et calcule un score de compatibilité avec chaque offre."
        
        elif any(w in message_lower for w in ['contact', 'aide', 'support']):
            return "Pour nous contacter: support@recrut-ai.com"
        
        else:
            return "Je suis là pour vous aider avec vos questions sur le recrutement. Pouvez-vous préciser votre demande?"
    
    def reset_conversation(self):
        """Réinitialise l'historique"""
        self.conversation_history = []

# Instance globale
chatbot = RecruitmentChatbot()