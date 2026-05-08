# Module de Matching CV - Offre
# Calcul de la compatibilité entre CV et offres

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class CVMatcher:
    """Matcher de CV avec les offres d'emploi"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
    
    def calculate_score(self, cv_text, offer_text):
        """
        Calcule le score de compatibilité entre un CV et une offre
        
        Args:
            cv_text: Texte du CV
            offer_text: Description de l'offre
        
        Returns:
            float: Score entre 0 et 1
        """
        try:
            # Vectoriser les textes
            texts = [cv_text, offer_text]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calculer la similarité cosinus
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            print(f"Erreur dans le calcul de score: {e}")
            return 0.0
    
    def match_cv_with_offer(self, cv_info, offer_info):
        """
        Matching avancé basé sur les compétences extraites
        
        Args:
            cv_info: Dict avec informations extraites du CV
            offer_info: Dict avec informations de l'offre
        
        Returns:
            dict: Détails du matching et score global
        """
        
        # Score de compétences
        cv_skills = set(cv_info.get('skills', []))
        required_skills = set(offer_info.get('required_skills', []))
        
        if required_skills:
            matched_skills = cv_skills.intersection(required_skills)
            skills_score = len(matched_skills) / len(required_skills)
        else:
            skills_score = 0.5
        
        # Score d'expérience
        cv_years = cv_info.get('years_experience', 0)
        min_years = offer_info.get('min_experience', 0)
        
        if cv_years >= min_years:
            experience_score = min(1.0, cv_years / (min_years + 5))
        else:
            experience_score = max(0.0, cv_years / (min_years + 1))
        
        # Score textuel
        cv_text = cv_info.get('full_text', '')
        offer_text = offer_info.get('description', '')
        textual_score = self.calculate_score(cv_text, offer_text)
        
        # Score global (moyenne pondérée)
        global_score = (
            skills_score * 0.50 +
            experience_score * 0.25 +
            textual_score * 0.25
        )
        
        return {
            'global_score': min(1.0, global_score),
            'skills_score': skills_score,
            'experience_score': experience_score,
            'textual_score': textual_score,
            'matched_skills': list(cv_skills.intersection(required_skills)),
            'missing_skills': list(required_skills - cv_skills),
            'recommendation': self._get_recommendation(global_score)
        }
    
    def rank_candidates(self, candidates, offer_info):
        """
        Classe les candidats selon leur compatibilité
        
        Args:
            candidates: Liste de CV analysés
            offer_info: Info de l'offre
        
        Returns:
            list: Candidats triés par score décroissant
        """
        
        scored_candidates = []
        
        for candidate in candidates:
            score_info = self.match_cv_with_offer(candidate['cv_info'], offer_info)
            scored_candidates.append({
                'candidate_id': candidate['id'],
                'name': candidate['name'],
                **score_info
            })
        
        # Trier par score décroissant
        return sorted(scored_candidates, key=lambda x: x['global_score'], reverse=True)
    
    def _get_recommendation(self, score):
        """Recommandation basée sur le score"""
        if score >= 0.9:
            return "Excellente correspondance - À interviewer en priorité"
        elif score >= 0.75:
            return "Bonne correspondance - Recommandé"
        elif score >= 0.60:
            return "Correspondance acceptable - À considérer"
        else:
            return "Faible correspondance - Consulter manual"

# Instance globale
cv_matcher = CVMatcher()
