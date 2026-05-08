# Modèle Offre d'Emploi

from extensions import db
from datetime import datetime, timedelta

class Offer(db.Model):
    """Modèle d'une offre d'emploi"""
    
    __tablename__ = 'offers'
    
    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Informations de l'offre
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)  # En JSON
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    
    # Détails
    job_type = db.Column(db.String(50))  # 'CDI', 'CDD', 'Stage', 'Freelance'
    min_salary = db.Column(db.Float)
    max_salary = db.Column(db.Float)
    min_experience = db.Column(db.Integer, default=0)  # En années
    
    # Statut
    is_active = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='open')  # 'open', 'closed', 'filled'
    
    # Compétences requises
    required_skills = db.Column(db.String(500))  # Comma-separated
    preferred_skills = db.Column(db.String(500))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deadline = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))
    
    # Relations
    applications = db.relationship('Application', backref='offer', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Offer {self.title}>'
    
    def is_deadline_passed(self):
        return datetime.utcnow() > self.deadline
    
    def get_required_skills_list(self):
        return [s.strip() for s in self.required_skills.split(',') if s.strip()] if self.required_skills else []
    
    def application_count(self):
        return len(self.applications)
