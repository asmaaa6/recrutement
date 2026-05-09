# Module de Matching CV - Offre - Powered by Claude AI
import os
import json
import anthropic

class CVMatcher:
    """Matcher de CV avec les offres d'emploi via Claude AI"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get('ANTHROPIC_API_KEY')
        )
    
    def calculate_score(self, cv_text, offer_text):
        """Calcule le score de compatibilité via Claude"""
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"""Compare ce CV avec cette offre et retourne UNIQUEMENT un JSON:
{{
    "global_score": 0.85,
    "skills_score": 0.90,
    "experience_score": 0.80,
    "textual_score": 0.85,
    "matched_skills": ["Python", "Flask"],
    "missing_skills": ["Docker"],
    "recommendation": "Bonne correspondance - Recommandé"
}}

CV:
{cv_text}

Offre:
{offer_text}"""
                }]
            )
            
            result = message.content[0].text
            return json.loads(result)
            
        except Exception as e:
            print(f"Erreur matching: {e}")
            return self._fallback_score(cv_text, offer_text)
    
    def match_cv_with_offer(self, cv_info, offer_info):
        """Matching complet basé sur les infos extraites"""
        cv_text = cv_info.get('full_text', '')
        offer_text = offer_info.get('description', '')
        result = self.calculate_score(cv_text, offer_text)
        cv_skills = set(cv_info.get('skills', []))
        required_skills = set(offer_info.get('required_skills', []))
        if required_skills:
            result['matched_skills'] = list(cv_skills & required_skills)
            result['missing_skills'] = list(required_skills - cv_skills)
        return result
    
    def rank_candidates(self, candidates, offer_info):
        """Classe les candidats par score décroissant"""
        scored_candidates = []
        for candidate in candidates:
            score_info = self.match_cv_with_offer(
                candidate['cv_info'], offer_info
            )
            scored_candidates.append({
                'candidate_id': candidate['id'],
                'name': candidate['name'],
                **score_info
            })
        return sorted(
            scored_candidates,
            key=lambda x: x['global_score'],
            reverse=True
        )
    
    def _fallback_score(self, cv_text, offer_text):
        """Score basique sans API"""
        cv_words = set(cv_text.lower().split())
        offer_words = set(offer_text.lower().split())
        if not offer_words:
            score = 0.5
        else:
            common = cv_words & offer_words
            score = min(1.0, len(common) / len(offer_words))
        return {
            'global_score': score,
            'skills_score': score,
            'experience_score': score,
            'textual_score': score,
            'matched_skills': [],
            'missing_skills': [],
            'recommendation': self._get_recommendation(score)
        }
    
    def _get_recommendation(self, score):
        if score >= 0.9:
            return "Excellente correspondance - À interviewer en priorité"
        elif score >= 0.75:
            return "Bonne correspondance - Recommandé"
        elif score >= 0.60:
            return "Correspondance acceptable - À considérer"
        return "Faible correspondance - Consulter manuellement"

cv_matcher = CVMatcher()