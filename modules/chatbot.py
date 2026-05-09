"""Chatbot (réponses simples prédéfinies, sans API)

Le template `templates/chatbot.html` simule actuellement côté client.
On fournit quand même une classe simple utilisable côté backend si besoin.
"""

from __future__ import annotations

import re
from typing import Dict


_RESPONSES = [
    (
        re.compile(r"\b(bonjour|salut|hello|hey)\b", re.IGNORECASE),
        "Bonjour ! Bienvenue sur RecrutAI. Comment puis-je vous aider ?",
    ),
    (
        re.compile(r"\b(offre|emploi|poste|vacance)\b", re.IGNORECASE),
        "Pour voir les offres, allez dans la section correspondante après connexion. Vous pouvez consulter les exigences et postuler.",
    ),
    (
        re.compile(r"\b(cv|candidature|candidats?)\b", re.IGNORECASE),
        "Pour déposer un CV, utilisez la page Upload CV. Le système extrait le texte puis calcule un score de matching avec les offres.",
    ),
    (
        re.compile(r"\b(score|matching|compatibilit(e|é))\b", re.IGNORECASE),
        "Le score est calculé automatiquement en comparant les compétences/texte du CV à ceux de l'offre (TF-IDF + cosinus).",
    ),
    (
        re.compile(r"\b(aide|support|contact)\b", re.IGNORECASE),
        "Contact support : info@recrutai.com (ou via la page Contact de votre interface).",
    ),
    (
        re.compile(r"\b(processus|etapes|étapes|d(é|)lais|temps)\b", re.IGNORECASE),
        "Le processus typique : 1) Analyse du CV 2) Matching 3) Évaluation 4) Décision. Les délais dépendent du volume et du poste.",
    ),
]


class RecruitmentChatbot:
    def __init__(self):
        pass

    def get_response(self, user_message: str) -> str:
        msg = user_message or ""
        for pattern, response in _RESPONSES:
            if pattern.search(msg):
                return response
        return "Merci pour votre question ! Dites-moi sur quel sujet vous voulez de l'aide : offres, CV, matching ou étapes du recrutement."


chatbot = RecruitmentChatbot()

