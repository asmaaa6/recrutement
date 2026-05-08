from flask import Flask, render_template, request, jsonify, session, redirect, url_for 
from flask_login import login_required, current_user, login_user, logout_user
from extensions import db, login_manager
from config import config
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

# Initialisation Flask
app = Flask(__name__)
environment = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[environment])

# Initialisation extensions
db.init_app(app)
login_manager.init_app(app)

# Création dossiers
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import des modèles (important pour db.create_all())
from models.user import User
from models.offer import Offer
from models.application import Application
from models.cv import CV

"""a Apprendre pour soualah 
Voici ce que ces lignes signifient (c'est ce que tu devras expliquer à ton encadrante) :
​Lignes 1 à 7 : Tu importes les outils. Par exemple, Flask sert à créer le site web, et werkzeug.security sert à cacher les mots de passe des utilisateurs pour que ce soit sécurisé.
​Ligne 10 : Tu crées officiellement l'application.
​Lignes 22 à 24 : C'est très important ! Ton application prépare les tables de ta base de données pour les Utilisateurs (User), les Offres d'emploi (Offer) et les Candidatures (Application).
"""

# ============================================
# FLASK-LOGIN USER LOADER
# ============================================

@login_manager.user_loader
def load_user(user_id):
    """Charger l'utilisateur par son ID"""
    return User.query.get(int(user_id))

# ============================================
# ROUTES PRINCIPALES
# ============================================

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            return render_template('login.html', error='Email et mot de passe requis'), 400
        
        # Chercher l'utilisateur par email ou username
        user = User.query.filter(
            (User.email == email) | (User.username == email)
        ).first()
        
        if user and check_password_hash(user.password_hash, password):
            # Connexion réussie
            login_user(user, remember=request.form.get('remember'))
            user.update_last_login()
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Email ou mot de passe incorrect'), 401
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Page d'inscription"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('confirm_password', '')
        role = request.form.get('role', 'candidate')
        
        # Validation
        if not all([username, email, password, password_confirm]):
            return render_template('signup.html', error='Tous les champs sont requis'), 400
        
        if len(password) < 6:
            return render_template('signup.html', error='Le mot de passe doit contenir au moins 6 caractères'), 400
        
        if password != password_confirm:
            return render_template('signup.html', error='Les mots de passe ne correspondent pas'), 400
        
        # Vérifier si l'utilisateur existe déjà
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return render_template('signup.html', error='Cet utilisateur ou email existe déjà'), 400
        
        # Créer l'utilisateur
        try:
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                role=role if role in ['candidate', 'recruiter', 'admin'] else 'candidate'
            )
            db.session.add(new_user)
            db.session.commit()
            
            # Logguer automatiquement après inscription
            login_user(new_user)
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            return render_template('signup.html', error=f'Erreur lors de l\'inscription: {str(e)}'), 500
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    """Déconnexion"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    """Profil utilisateur"""
    return render_template('profile.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Tableau de bord candidat"""
    return render_template('dashboard.html')

@app.route('/recruiter-dashboard')
@login_required
def recruiter_dashboard():
    """Tableau de bord recruteur"""
    if current_user.role != 'recruiter':
        return redirect(url_for('index'))
    return render_template('recruiter-dashboard.html')

@app.route('/cv-upload', methods=['GET', 'POST'])
@login_required
def cv_upload():
    """Upload de CV"""
    if request.method == 'POST':
        # Logique d'upload à implémenter
        pass
    return render_template('cv-upload.html')

@app.route('/cv-analysis')
@login_required
def cv_analysis():
    """Analyse de CV"""
    return render_template('cv-analysis.html')

@app.route('/chatbot')
@login_required
def chatbot():
    """Interface chatbot"""
    return render_template('chatbot.html')

# ============================================
# GESTION DES ERREURS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Page 404"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Page 500"""
    return render_template('500.html'), 500

@app.shell_context_processor
def make_shell_context():
    """Contexte shell Flask"""
    return {'db': db}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8080)
