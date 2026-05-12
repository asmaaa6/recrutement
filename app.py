import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, redirect, url_for, request

from flask_login import login_required, current_user

from extensions import db, login_manager
from config import config
from models.user import User

# Import blueprints
from modules.auth import auth_bp
from modules.applications import applications_bp
from modules.offers import offers_bp


# API JSON (chatbot / analyse de CV)
from modules.chatbot import chatbot as recruitment_chatbot

app = Flask(__name__)


environnement = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[environnement])

db.init_app(app)
login_manager.init_app(app)

# Ensure DB tables exist
# Import models so SQLAlchemy can resolve relationships correctly
from models.application import Application  # noqa: E402
from models.offer import Offer  # noqa: E402
from models.cv import CV  # noqa: E402

with app.app_context():
    db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(applications_bp)
app.register_blueprint(offers_bp)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('recruiter_dashboard'))


@app.route('/recruiter-dashboard')
@login_required
def recruiter_dashboard():
    if current_user.role != 'recruiter':
        return redirect(url_for('index'))
    return render_template('recruiter-dashboard.html')


@app.route('/chatbot', methods=['GET'])
@login_required
def chatbot_page():
    return render_template('chatbot.html')


@app.route('/api/chatbot', methods=['POST'])
@login_required
def api_chatbot():
    # Corps de la requête: {"message": "..."}
    donnees = request.get_json(silent=True) or {}
    message = donnees.get('message') or donnees.get('msg') or ""
    reponse = recruitment_chatbot.get_response(message)
    return {"response": reponse}


@app.route('/api/cv-analysis', methods=['GET'])
@login_required
def api_cv_analysis():
    # Endpoint simple pour l'interface : retourne les données extraites du CV.
    from models.cv import CV
    import json

    cv = CV.query.filter_by(user_id=current_user.id).first()
    if not cv or not cv.is_analyzed:
        return {"error": "no_cv"}, 404

    return {
        "skills": json.loads(cv.skills) if cv.skills else [],
        "education": json.loads(cv.education) if cv.education else [],
        "experience": json.loads(cv.experience) if cv.experience else [],
        "languages": json.loads(cv.languages) if cv.languages else [],
        "cv_score": float(getattr(cv, "analysis_score", 0.0) or 0.0),
    }



# Backward compatible aliases (if any old code links directly)
@app.route('/cv-upload', methods=['GET'])
@login_required
def cv_upload_alias_get():
    return redirect(url_for('applications.cv_upload'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

