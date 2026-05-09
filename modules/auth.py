"""Gestion des utilisateurs (auth) pour RecrutAI.

Objectif:
- 2 rôles: candidat / recruteur
- Signup + Login complets
- Redirection selon le rôle après login

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

    username = (request.form.get("username") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    password_confirm = request.form.get("confirm_password") or request.form.get("password_confirm") or ""

    role = (request.form.get("role") or "candidate").strip().lower()
    if role not in {"candidate", "recruiter", "admin"}:
        role = "candidate"

    if not all([username, email, password, password_confirm]):
        return render_template("signup.html", error="Tous les champs sont requis"), 400

    if len(password) < 6:
        return render_template("signup.html", error="Le mot de passe doit contenir au moins 6 caractères"), 400

    if password != password_confirm:
        return render_template("signup.html", error="Les mots de passe ne correspondent pas"), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return render_template("signup.html", error="Cet utilisateur ou email existe déjà"), 400

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
        return redirect(url_for("recruiter_dashboard")) if new_user.role == "recruiter" else redirect(url_for("dashboard"))
    except Exception as e:
        db.session.rollback()
        return render_template("signup.html", error=f"Erreur lors de l'inscription: {e}"), 500


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email_or_username = (request.form.get("email") or request.form.get("username") or "").strip().lower()
    password = request.form.get("password") or ""
    remember = bool(request.form.get("remember"))

    if not email_or_username or not password:
        return render_template("login.html", error="Email et mot de passe requis"), 400

    user = User.query.filter((User.email == email_or_username) | (User.username == email_or_username)).first()

    if not user or not check_password_hash(user.password_hash, password):
        return render_template("login.html", error="Email ou mot de passe incorrect"), 401

    login_user(user, remember=remember)
    user.update_last_login()

    return redirect(url_for("recruiter_dashboard")) if user.role == "recruiter" else redirect(url_for("dashboard"))


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

