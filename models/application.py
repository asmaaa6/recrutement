# Modèle Candidature

from extensions import db
from datetime import datetime

class Application(db.Model):
    """Modèle d'une candidature"""
    
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offers.id'), nullable=False, index=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cvs.id'))
    
    # Statut de la candidature
    status = db.Column(db.String(50), default='pending')  
    # 'pending', 'under_review', 'shortlisted', 'accepted', 'rejected', 'withdrawn'
    
    # Scores
    cv_score = db.Column(db.Float, default=0.0)  # Score de qualité du CV (0-1)
    match_score = db.Column(db.Float, default=0.0)  # Score de matching (0-1)
    overall_score = db.Column(db.Float, default=0.0)  # Score global (0-1)
    
    # Commentaires
    recruiter_notes = db.Column(db.Text)
    candidate_message = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    
    # Interview
    interview_date = db.Column(db.DateTime)
    interview_notes = db.Column(db.Text)
    interview_score = db.Column(db.Float)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'offer_id', name='unique_user_offer'),
    )
    
    def __repr__(self):
        return f'<Application {self.user_id} for {self.offer_id}>'
    
    def is_recent(self, days=7):
        """Vérifie si la candidature est récente"""
        return (datetime.utcnow() - self.created_at).days <= days
    
    def can_withdraw(self):
        """Vérifie si la candidature peut être retirée"""
        return self.status in ['pending', 'under_review']
    
    def get_status_badge_color(self):
        """Retourne la couleur du badge de statut"""
        colors = {
            'pending': 'warning',
            'under_review': 'info',
            'shortlisted': 'primary',
            'accepted': 'success',
            'rejected': 'danger',
            'withdrawn': 'secondary'
        }
        return colors.get(self.status, 'secondary')
