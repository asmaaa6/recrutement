# Module d'Analyse de CV
# Extraction d'informations, reconnaissance de compétences, etc.

from utils.pdf_extractor import extract_text_from_pdf
from utils.text_processor import process_cv_text
import spacy

class CVAnalyzer:
    """Analyseur de CV utilisant NLP"""
    
    def __init__(self):
        self.nlp = None
        try:
            self.nlp = spacy.load('fr_core_news_sm')
        except:
            print("Modèle spaCy non trouvé. À installer avec: python -m spacy download fr_core_news_sm")
    
    def analyze_cv(self, file_path):
        """Analyse complète d'un CV"""
        try:
            # Extraire le texte
            text = extract_text_from_pdf(file_path) if file_path.endswith('.pdf') else self._read_text_file(file_path)
            
            # Traiter le texte
            processed_text = process_cv_text(text)
            
            # Extraire les informations
            info = {
                'full_text': processed_text,
                'skills': self.extract_skills(processed_text),
                'education': self.extract_education(processed_text),
                'experience': self.extract_experience(processed_text),
                'contact_info': self.extract_contact_info(text),
                'languages': self.extract_languages(processed_text)
            }
            
            return info
        
        except Exception as e:
            print(f"Erreur lors de l'analyse: {e}")
            return None
    
    def extract_skills(self, text):
        """Détection automatique des compétences"""
        # Keywords courants dans le recrutement tech
        skills_keywords = {
            'Python': ['python', 'django', 'flask', 'fastapi'],
            'JavaScript': ['javascript', 'typescript', 'nodejs', 'react', 'vue'],
            'SQL': ['sql', 'mysql', 'postgresql', 'mongodb'],
            'Machine Learning': ['machine learning', 'deep learning', 'tensorflow', 'keras'],
            'Docker': ['docker', 'kubernetes', 'container'],
            'Git': ['git', 'github', 'gitlab', 'version control'],
            # À étendre...
        }
        
        detected_skills = []
        text_lower = text.lower()
        
        for skill, keywords in skills_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_skills.append(skill)
        
        return detected_skills
    
    def extract_education(self, text):
        """Détection des diplômes"""
        education_keywords = ['licence', 'master', 'ingénieur', 'bac', 'diplôme', 'certification']
        # À implémenter avec spaCy pour une meilleure détection
        return []
    
    def extract_experience(self, text):
        """Détection des expériences"""
        # À implémenter
        return []
    
    def extract_contact_info(self, text):
        """Extraction des coordonnées"""
        import re
        
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        phones = re.findall(r'(?:\+33|0)[1-9](?:[0-9]{8}|[0-9]{9})', text)
        
        return {
            'emails': emails,
            'phones': phones
        }
    
    def extract_languages(self, text):
        """Détection des langues parlées"""
        languages = {
            'Français': ['français', 'langue maternelle'],
            'Anglais': ['anglais', 'english', 'fluent english'],
            'Espagnol': ['espagnol', 'spanish'],
            'Allemand': ['allemand', 'german'],
        }
        
        detected = []
        text_lower = text.lower()
        
        for lang, keywords in languages.items():
            if any(keyword in text_lower for keyword in keywords):
                detected.append(lang)
        
        return detected
    
    def _read_text_file(self, file_path):
        """Lecture d'un fichier texte"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""

# Instance globale
cv_analyzer = CVAnalyzer()
