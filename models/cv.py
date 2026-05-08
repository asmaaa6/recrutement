# Modèle CV

from extensions import db
from datetime import datetime

class CV(db.Model):
    """Modèle de CV stocké"""
    
    __tablename__ = 'cvs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False, index=True)
    
    # Fichier
    file_path = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)  # en bytes
    file_type = db.Column(db.String(10))  # 'pdf', 'doc', 'docx', 'txt'
    
    # Contenu extrait
    raw_text = db.Column(db.Text)  # Texte brut du CV
    processed_text = db.Column(db.Text)  # Texte traité/nettoyé
    
    # Données structurées extraites
    full_name = db.Column(db.String(200))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(200))
    
    # Listes d'informations (JSON)
    skills = db.Column(db.Text)  # JSON array
    education = db.Column(db.Text)  # JSON array
    experience = db.Column(db.Text)  # JSON array
    languages = db.Column(db.Text)  # JSON array
    certifications = db.Column(db.Text)  # JSON array
    
    # Métadonnées
    analysis_score = db.Column(db.Float, default=0.0)  # Score de qualité (0-1)
    is_analyzed = db.Column(db.Boolean, default=False)
    analysis_date = db.Column(db.DateTime)
    
    years_experience = db.Column(db.Float)
    last_position = db.Column(db.String(200))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    applications = db.relationship('Application', backref='cv_file')
    
    def __repr__(self):
        return f'<CV {self.user_id}>'
    
    def get_skills_list(self):
        """Retourne la liste des compétences"""
        import json
        try:
            return json.loads(self.skills) if self.skills else []
        except:
            return []
    
    def get_education_list(self):
        """Retourne la liste de l'éducation"""
        import json
        try:
            return json.loads(self.education) if self.education else []
        except:
            return []
    
    def get_experience_list(self):
        """Retourne la liste des expériences"""
        import json
        try:
            return json.loads(self.experience) if self.experience else []
        except:
            return []
