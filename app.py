import os
import sys

# Cette ligne force Vercel à lire les fichiers dans ton dossier
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify, session, redirect, url_for 
from flask_login import login_required, current_user, login_user, logout_user

# Import sécurisé pour Vercel
try:
    from extensions import db, login_manager
    from config import config
    from models.user import User
    from models.offer import Offer
    from models.application import Application
    from models.cv import CV
except ImportError:
    from .extensions import db, login_manager
    from .config import config
    from .models.user import User
    from .models.offer import Offer
    from .models.application import Application
    from .models.cv import CV

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

# Configuration
environment = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[environment])

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# On retire le db.create_all() qui fait planter Vercel au démarrage
if __name__ == '__main__':
    app.run(debug=True)