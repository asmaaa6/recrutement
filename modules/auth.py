"""Authentification (login/register complets)

- 2 rôles: recruiter et candidate
- Stockage: models.user.User
- Gestion Flask-Login

Routes exposées:
- GET/POST /auth/register
- GET/POST /auth/login
- GET /auth/logout
"""

from __future__ import annotations

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager
from models.user import User


auth_bp = Blueprint("auth", __name__, url_prefix="")  # on expose en /login et /signup ?


def _render_with_error(template: str, error: str):
    return render_template(template, error=error), 400


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = (request.form.get("username") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    password_confirm = request.form.get("confirm_password") or request.form.get("password_confirm") or ""
    role = (request.form.get("role") or "candidate").strip()
    if role not in {"candidate", "recruiter", "admin"}:
        role = "candidate"

    if not username or not email or not password or not password_confirm:
        return _render_with_error("signup.html", "Tous les champs sont requis" )

    if len(password) < 6:
        return _render_with_error("signup.html", "Le mot de passe doit contenir au moins 6 caractères")

    if password != password_confirm:
        return _render_with_error("signup.html", "Les mots de passe ne correspondent pas")

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return _render_with_error("signup.html", "Cet utilisateur ou email existe déjà")

    try:
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role if role in {"candidate", "recruiter", "admin"} else "candidate",
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        new_user.update_last_login()
        return redirect(url_for("dashboard"))
    except Exception as e:
        db.session.rollback()
        return _render_with_error("signup.html", f"Erreur lors de l'inscription: {e}")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email_or_username = (request.form.get("email") or request.form.get("username") or "").strip().lower()
    password = request.form.get("password") or ""
    remember = request.form.get("remember")

    if not email_or_username or not password:
        return _render_with_error("login.html", "Email et mot de passe requis")

    user = User.query.filter((User.email == email_or_username) | (User.username == email_or_username)).first()

    if not user or not check_password_hash(user.password_hash, password):
        return _render_with_error("login.html", "Email ou mot de passe incorrect")

    login_user(user, remember=bool(remember))
    user.update_last_login()

    # redirection selon rôle
    if user.role == "recruiter":
        return redirect(url_for("recruiter_dashboard"))
    return redirect(url_for("dashboard"))


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@auth_bp.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@auth_bp.route("/settings", methods=["GET"])
@login_required
def settings():
    return render_template("profile.html", user=current_user)

