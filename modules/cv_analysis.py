# Module d'Analyse de CV - Powered by Claude AI
import os
import re
import json
import anthropic

class CVAnalyzer:
    """Analyseur de CV utilisant l'API Claude"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get('ANTHROPIC_API_KEY')
        )
    
    def analyze_cv(self, file_path):
        """Analyse complète d'un CV"""
        try:
            text = self._read_file(file_path)
            
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"""Analyse ce CV et retourne UNIQUEMENT un JSON:
{{
    "skills": ["skill1", "skill2"],
    "education": ["diplome1"],
    "experience": ["experience1"],
    "languages": ["langue1"],
    "contact_info": {{
        "emails": ["email@example.com"],
        "phones": ["0600000000"]
    }},
    "years_experience": 3,
    "full_text": "résumé du profil en 2 phrases"
}}

CV:
{text}"""
                }]
            )
            
            result = message.content[0].text
            return json.loads(result)
            
        except Exception as e:
            print(f"Erreur analyse CV: {e}")
            return self._fallback_analysis(file_path)
    
    def _fallback_analysis(self, file_path):
        """Analyse basique sans API"""
        text = self._read_file(file_path)
        return {
            'skills': self._extract_skills_basic(text),
            'education': [],
            'experience': [],
            'languages': self._extract_languages_basic(text),
            'contact_info': self._extract_contact_info(text),
            'years_experience': 0,
            'full_text': text[:500]
        }
    
    def _extract_skills_basic(self, text):
        skills_keywords = {
            'Python': ['python', 'django', 'flask'],
            'JavaScript': ['javascript', 'react', 'vue'],
            'SQL': ['sql', 'mysql', 'postgresql'],
            'Machine Learning': ['machine learning', 'deep learning'],
            'Docker': ['docker', 'kubernetes'],
            'Git': ['git', 'github', 'gitlab'],
        }
        detected = []
        text_lower = text.lower()
        for skill, keywords in skills_keywords.items():
            if any(k in text_lower for k in keywords):
                detected.append(skill)
        return detected
    
    def _extract_languages_basic(self, text):
        languages = {
            'Français': ['français', 'french'],
            'Anglais': ['anglais', 'english'],
            'Arabe': ['arabe', 'arabic'],
        }
        detected = []
        text_lower = text.lower()
        for lang, keywords in languages.items():
            if any(k in text_lower for k in keywords):
                detected.append(lang)
        return detected
    
    def _extract_contact_info(self, text):
        emails = re.findall(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        phones = re.findall(r'(?:\+213|0)[1-9][0-9]{8}', text)
        return {'emails': emails, 'phones': phones}
    
    def _read_file(self, file_path):
        try:
            if file_path.endswith('.pdf'):
                from PyPDF2 import PdfReader
                reader = PdfReader(file_path)
                return ' '.join([page.extract_text() for page in reader.pages])
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except:
            return ""

cv_analyzer = CVAnalyzer()