import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, redirect, url_for
from flask_login import login_required, current_user

from extensions import db, login_manager
from config import config
from models.user import User

# Import blueprints
from modules.auth import auth_bp
from modules.applications import applications_bp

app = Flask(__name__)

environment = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[environment])

db.init_app(app)
login_manager.init_app(app)

# Ensure DB tables exist
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(applications_bp)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    # simple routing: candidate users see dashboard.html, recruiters see recruiter-dashboard.html
    if current_user.role == 'recruiter':
        return redirect(url_for('recruiter_dashboard'))
    return render_template('dashboard.html')


@app.route('/recruiter-dashboard')
@login_required
def recruiter_dashboard():
    if current_user.role != 'recruiter':
        return redirect(url_for('dashboard'))
    return render_template('recruiter-dashboard.html')


@app.route('/chatbot', methods=['GET'])
@login_required
def chatbot_page():
    return render_template('chatbot.html')


# Backward compatible aliases (if any old code links directly)
@app.route('/cv-upload', methods=['GET'])
@login_required
def cv_upload_alias_get():
    return redirect(url_for('applications.cv_upload'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

