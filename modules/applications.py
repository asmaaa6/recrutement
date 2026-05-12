"""Gestion des candidatures / upload CV (par recruteur)

Routes exposées:
- GET /cv-upload
- POST /cv-upload

Fonctionnement demandé:
- Le recruteur uploade les CV des candidats
- Extraction du texte via modules.cv_analysis (regex + PyPDF2)
- Stockage dans models.CV

Ensuite:
- On redirige vers /cv-analysis pour afficher un aperçu.
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from extensions import db
from models.cv import CV
from modules.cv_analysis import cv_analyzer


applications_bp = Blueprint("applications", __name__, url_prefix="")


def _extension_autorisee(nom_fichier: str) -> bool:
    extensions_autorisees = {"pdf", "txt", "doc", "docx"}
    extension = (nom_fichier.rsplit(".", 1)[-1] if "." in nom_fichier else "").lower()
    return extension in extensions_autorisees


@applications_bp.route("/cv-upload", methods=["GET", "POST"])
@login_required
def televerser_cv():
    # Seul le recruteur peut uploader un CV
    if current_user.role != "recruiter":
        flash("Accès refusé : seul le recruteur peut téléverser des CV.", "danger")
        return redirect(url_for("recruiter_dashboard"))

    if request.method == "GET":
        return render_template("cv-upload.html")

    if "cv_file" not in request.files:
        flash("Aucun fichier envoyé.", "danger")
        return redirect(url_for("cv_upload"))

    fichier_cv = request.files["cv_file"]
    if not fichier_cv or fichier_cv.filename == "":
        flash("Fichier vide.", "danger")
        return redirect(url_for("cv_upload"))

    if not _extension_autorisee(fichier_cv.filename):
        flash("Format non autorisé. Utilisez PDF/TXT/DOC/DOCX.", "danger")
        return redirect(url_for("cv_upload"))

    nom_fichier = secure_filename(fichier_cv.filename)
    repertoire_televersement = current_app.config["UPLOAD_FOLDER"]  # type: ignore[name-defined]
    os.makedirs(repertoire_televersement, exist_ok=True)

    nom_fichier_unique = f"{current_user.id}_{int(datetime.utcnow().timestamp())}_{nom_fichier}"
    chemin_fichier = os.path.join(repertoire_televersement, nom_fichier_unique)
    fichier_cv.save(chemin_fichier)

    # Extraction du texte et analyse
    analyse_cv = cv_analyzer.analyze_cv(chemin_fichier)

    cv_existant = CV.query.filter_by(user_id=current_user.id).first()
    cv_enregistree = cv_existant if cv_existant else CV(user_id=current_user.id, file_path="", original_filename="")
    cv_enregistree.file_path = chemin_fichier
    cv_enregistree.original_filename = nom_fichier
    cv_enregistree.file_size = os.path.getsize(chemin_fichier)
    cv_enregistree.file_type = nom_fichier.rsplit(".", 1)[-1].lower()
    cv_enregistree.raw_text = analyse_cv.get("raw_text")
    cv_enregistree.processed_text = analyse_cv.get("processed_text")

    infos_contact = analyse_cv.get("contact_info") or {}
    cv_enregistree.email = (infos_contact.get("emails") or [""])[0]
    cv_enregistree.phone = (infos_contact.get("phones") or [""])[0]
    cv_enregistree.skills = __import__("json").dumps(analyse_cv.get("skills") or [])
    cv_enregistree.education = __import__("json").dumps(analyse_cv.get("education") or [])
    cv_enregistree.experience = __import__("json").dumps(analyse_cv.get("experience") or [])
    cv_enregistree.languages = __import__("json").dumps(analyse_cv.get("languages") or [])

    cv_enregistree.years_experience = float(analyse_cv.get("years_experience") or 0.0)

    # Score d'analyse basé sur les informations détectées
    competences_count = len(analyse_cv.get("skills") or [])
    langues_count = len(analyse_cv.get("languages") or [])
    experience_count = len(analyse_cv.get("experience") or [])
    formation_count = len(analyse_cv.get("education") or [])

    part_competences = min(competences_count / 15.0, 1.0) * 0.45
    part_langues = min(langues_count / 5.0, 1.0) * 0.15
    part_experience = min(experience_count / 8.0, 1.0) * 0.25
    part_formation = min(formation_count / 5.0, 1.0) * 0.15
    cv_enregistree.analysis_score = float(max(0.0, min(part_competences + part_langues + part_experience + part_formation, 1.0)))

    cv_enregistree.is_analyzed = True
    cv_enregistree.analysis_date = datetime.utcnow()
    db.session.add(cv_enregistree)
    db.session.commit()

    flash("CV téléversé et analysé.", "success")
    return redirect(url_for("cv_analysis"))


@applications_bp.route("/cv-analysis", methods=["GET"])
@login_required
def cv_analysis():
    cv = CV.query.filter_by(user_id=current_user.id).first()
    if not cv or not cv.is_analyzed:
        flash("Aucun CV analysé pour ce compte.", "warning")
        return redirect(url_for("cv_upload"))

    import json

    competences = json.loads(cv.skills) if cv.skills else []
    formations = json.loads(cv.education) if cv.education else []
    experiences = json.loads(cv.experience) if cv.experience else []
    langues = json.loads(cv.languages) if cv.languages else []

    return render_template(
        "cv-analysis.html",
        skills=competences,
        education=formations,
        experience=experiences,
        languages=langues,
        cv_score=getattr(cv, "analysis_score", 0.0) or 0.0,
    )

