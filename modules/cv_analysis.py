"""Module d'analyse de CV (regex uniquement)

Objectif:
- Extraire le texte d'un PDF avec PyPDF2
- Nettoyer le texte
- Extraire les informations clés avec des expressions régulières

Sortie:
- dictionnaire avec clés: skills, education, experience, languages, contact_info, years_experience, full_text, processed_text
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


_PATTERNS_COMPETENCES: Dict[str, List[str]] = {
    "Python": [r"\bpython\b", r"\bdjango\b", r"\bflask\b"],
    "JavaScript": [r"\bjavascript\b", r"\bnode\.js\b", r"\breact\b", r"\bvue\.js\b"],
    "SQL": [r"\bsql\b", r"\bmysql\b", r"\bpostgresql\b", r"\bpostgres\b"],
    "HTML/CSS": [r"\bhtml\b", r"\bcss\b"],
    "Java": [r"\bjava\b"],
    "C/C++": [r"\bc\+\+\b", r"\bc\b"],
    "Machine Learning": [r"\bmachine learning\b", r"\bdeep learning\b", r"\bscikit[- ]learn\b"],
    "Data Analysis": [r"\bpandas\b", r"\bdata analysis\b", r"\bdata\s+analysis\b"],
    "Docker": [r"\bdocker\b", r"\bkubernetes\b"],
    "Git": [r"\bgit\b", r"\bgithub\b", r"\bgitlab\b"],
    "NLP": [r"\bnlp\b", r"\btransformers\b"],
}


_PATTERNS_LANGUES: Dict[str, List[str]] = {
    "Français": [r"\bfran(c|ç)ais\b", r"\bfrench\b"],
    "Anglais": [r"\benglish\b", r"\banglais\b"],
    "Arabe": [r"\barabe\b", r"\barabic\b"],
}


def _nettoyer_espaces(texte: str) -> str:
    texte = texte.replace("\u00a0", " ")
    texte = re.sub(r"[\t\r]+", " ", texte)
    texte = re.sub(r"\n{2,}", "\n", texte)
    texte = re.sub(r" +", " ", texte)
    return texte.strip()


def _extraire_emails(texte: str) -> List[str]:
    return list(
        dict.fromkeys(
            re.findall(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
                texte,
            )
        )
    )


def _extraire_telephones(texte: str) -> List[str]:
    # Exemple simple: France / Algérie, etc.
    telephones = re.findall(r"(?:\+213|0)[1-9][0-9]{8}\b", texte)
    return list(dict.fromkeys(telephones))


def _extraire_competences(texte: str) -> List[str]:
    texte_minuscule = texte.lower()
    trouves: List[str] = []
    for competence, patterns in _PATTERNS_COMPETENCES.items():
        for motif in patterns:
            if re.search(motif, texte_minuscule, flags=re.IGNORECASE):
                trouves.append(competence)
                break
    return list(dict.fromkeys(trouves))


def _extraire_langues(texte: str) -> List[str]:
    texte_minuscule = texte.lower()
    langues_trouvees: List[str] = []
    for langue, patterns in _PATTERNS_LANGUES.items():
        for motif in patterns:
            if re.search(motif, texte_minuscule, flags=re.IGNORECASE):
                langues_trouvees.append(langue)
                break
    return list(dict.fromkeys(langues_trouvees))


def _extraire_annees_experience(texte: str) -> float:
    # Heuristique : cherche "X ans" ou "X+ ans"
    match = re.search(r"\b(\d{1,2})\s*(?:\+\s*)?ans\b", texte, flags=re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except Exception:
            pass
    return 0.0


def _extraire_liste_section(texte: str, titres_section: List[str]) -> List[str]:
    # Extraction simple : prendre les premières lignes après un titre reconnu
    for titre in titres_section:
        motif = r"(?:^|\n)\s*" + re.escape(titre) + r"\s*[:\-]?\s*\n"
        match = re.search(motif, texte, flags=re.IGNORECASE)
        if not match:
            continue
        debut = match.end()
        extrait = texte[debut : debut + 800]
        items = [item.strip() for item in re.split(r"\n|•|\-\s", extrait) if item.strip()]
        items = [item for item in items if len(item) >= 6]
        return items[:10]
    return []


def _extraire_formation(texte: str) -> List[str]:
    return _extraire_liste_section(
        texte,
        ["Education", "Educations", "Diplômes", "Diplome", "Formation", "Formations"],
    )


def _extraire_experience(texte: str) -> List[str]:
    return _extraire_liste_section(
        texte,
        [
            "Experience",
            "Expérience",
            "Expérience professionnelle",
            "Professional Experience",
            "Expérience",
        ],
    )


def _lire_texte_fichier(chemin_fichier: str) -> str:
    if chemin_fichier.lower().endswith(".pdf"):
        from PyPDF2 import PdfReader

        lecteur = PdfReader(chemin_fichier)
        pages = []
        for page in lecteur.pages:
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
        return "\n".join(pages)

    if chemin_fichier.lower().endswith(".txt"):
        with open(chemin_fichier, "r", encoding="utf-8", errors="ignore") as fichier:
            return fichier.read()

    return ""


class AnalyseurCVRegex:
    def analyze_cv(self, chemin_fichier: str) -> Dict[str, Any]:
        texte_brut = _lire_texte_fichier(chemin_fichier)
        texte_nettoye = _nettoyer_espaces(texte_brut)

        emails = _extraire_emails(texte_nettoye)
        telephones = _extraire_telephones(texte_nettoye)

        competences = _extraire_competences(texte_nettoye)
        langues = _extraire_langues(texte_nettoye)

        formation = _extraire_formation(texte_nettoye)
        experience = _extraire_experience(texte_nettoye)

        annees_experience = _extraire_annees_experience(texte_nettoye)

        resume = texte_nettoye[:1200]

        return {
            "skills": competences,
            "education": formation,
            "experience": experience,
            "languages": langues,
            "contact_info": {"emails": emails, "phones": telephones},
            "years_experience": annees_experience,
            "full_text": resume,
            "processed_text": texte_nettoye,
            "raw_text": texte_brut,
        }


cv_analyzer = AnalyseurCVRegex()

