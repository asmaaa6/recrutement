"""Gestion des utilisateurs (auth) pour RecrutAI.

Objectif:
- Comptes recruteur uniquement
- Signup + Login sécurisés
- Redirection vers le tableau de bord recruteur après login

Routes:
- GET/POST /signup
- GET/POST /login
- GET /logout
- GET /profile
- GET /settings
"""

from __future__ import annotations

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models.user import User


auth_bp = Blueprint("auth", __name__, url_prefix="")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    nom_utilisateur = (request.form.get("username") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    mot_de_passe = request.form.get("password") or ""
    confirmation_mot_de_passe = request.form.get("confirm_password") or request.form.get("password_confirm") or ""

    if not all([nom_utilisateur, email, mot_de_passe, confirmation_mot_de_passe]):
        return render_template("signup.html", error="Tous les champs sont requis"), 400

    if len(mot_de_passe) < 6:
        return render_template("signup.html", error="Le mot de passe doit contenir au moins 6 caractères"), 400

    if mot_de_passe != confirmation_mot_de_passe:
        return render_template("signup.html", error="Les mots de passe ne correspondent pas"), 400

    if User.query.filter((User.username == nom_utilisateur) | (User.email == email)).first():
        return render_template("signup.html", error="Cet utilisateur ou email existe déjà"), 400

    try:
        nouvel_utilisateur = User(
            username=nom_utilisateur,
            email=email,
            password_hash=generate_password_hash(mot_de_passe),
            role="recruiter",
        )
        db.session.add(nouvel_utilisateur)
        db.session.commit()

        login_user(nouvel_utilisateur)
        nouvel_utilisateur.update_last_login()
        return redirect(url_for("recruiter_dashboard"))
    except Exception as e:
        db.session.rollback()
        return render_template("signup.html", error=f"Erreur lors de l'inscription: {e}"), 500


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    identifiant = (request.form.get("email") or request.form.get("username") or "").strip().lower()
    mot_de_passe = request.form.get("password") or ""
    se_souvenir = bool(request.form.get("remember"))

    if not identifiant or not mot_de_passe:
        return render_template("login.html", error="Email et mot de passe requis"), 400

    utilisateur = User.query.filter((User.email == identifiant) | (User.username == identifiant)).first()

    if not utilisateur or not check_password_hash(utilisateur.password_hash, mot_de_passe):
        return render_template("login.html", error="Email ou mot de passe incorrect"), 401

    if utilisateur.role != "recruiter":
        return render_template("login.html", error="Ce compte n'est pas autorisé. Créez un compte recruteur."), 403

    login_user(utilisateur, remember=se_souvenir)
    utilisateur.update_last_login()

    return redirect(url_for("recruiter_dashboard"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@auth_bp.route("/settings")
@login_required
def settings():
    # UI existante: profile.html
    return render_template("profile.html", user=current_user)

