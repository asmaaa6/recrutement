# Modèle Utilisateur

from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    """Modèle d'utilisateur"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='candidate')  # 'candidate', 'recruiter', 'admin'
    
    # Informations personnelles
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.Text)
    
    # Statut
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(255), unique=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relations
    cv = db.relationship('CV', backref='user', uselist=False, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='user', cascade='all, delete-orphan')
    offers = db.relationship('Offer', backref='recruiter', foreign_keys='Offer.recruiter_id', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()
