import sys; import os; sys.path.append(os.path.dirname(__file__))
from flask import Flask, render_template, request, jsonify, session, redirect, url_for 
from flask_login import login_required, current_user, login_user, logout_user
from .extensions import db, login_manager
from .config import config
from .models.user import User
from .models.offer import Offer
from .models.application import Application
from .models.cv import CV
from werkzeug.security import generate_password_hash, check_password_hash
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
        
        user = User.query.filter((User.email == email) | (User.username == email)).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=request.form.get('remember'))
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
        
        if not all([username, email, password, password_confirm]):
            return render_template('signup.html', error='Tous les champs sont requis'), 400
        
        if password != password_confirm:
            return render_template('signup.html', error='Les mots de passe ne correspondent pas'), 400
        
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return render_template('signup.html', error='Cet utilisateur ou email existe déjà'), 400
        
        try:
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                role=role if role in ['candidate', 'recruiter', 'admin'] else 'candidate'
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            return render_template('signup.html', error=f'Erreur: {str(e)}'), 500
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Gestion des erreurs
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8080)