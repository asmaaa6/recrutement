"""Module d'analyse de CV (regex uniquement)

Objectif:
- Extraire le texte d'un PDF avec PyPDF2
- Nettoyer le texte
- Extraire informations avec regex (pas d'API, pas spaCy)

Sortie:
- dict avec clés: skills, education, experience, languages, contact_info, years_experience, full_text, processed_text
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


_SKILL_PATTERNS: Dict[str, List[str]] = {
    # Web / Langages
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


_LANGUAGE_PATTERNS: Dict[str, List[str]] = {
    "Français": [r"\bfran(c|ç)ais\b", r"\bfrench\b"],
    "Anglais": [r"\benglish\b", r"\banglais\b"],
    "Arabe": [r"\barabe\b", r"\barabic\b"],
}


def _collapse_whitespace(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[\t\r]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r" +", " ", text)
    return text.strip()


def _extract_emails(text: str) -> List[str]:
    return list(
        dict.fromkeys(
            re.findall(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
                text,
            )
        )
    )


def _extract_phones(text: str) -> List[str]:
    # Support simple: Algérie (+213 XXXXXXXXX ou 0XXXXXXXXX)
    phones = re.findall(r"(?:\+213|0)[1-9][0-9]{8}\b", text)
    return list(dict.fromkeys(phones))


def _extract_skills(text: str) -> List[str]:
    text_l = text.lower()
    found: List[str] = []
    for skill, patterns in _SKILL_PATTERNS.items():
        for p in patterns:
            if re.search(p, text_l, flags=re.IGNORECASE):
                found.append(skill)
                break
    # Remove duplicates preserving order
    return list(dict.fromkeys(found))


def _extract_languages(text: str) -> List[str]:
    text_l = text.lower()
    found: List[str] = []
    for lang, patterns in _LANGUAGE_PATTERNS.items():
        for p in patterns:
            if re.search(p, text_l, flags=re.IGNORECASE):
                found.append(lang)
                break
    return list(dict.fromkeys(found))


def _extract_years_experience(text: str) -> float:
    # Heuristique: cherche "X ans" ou "\b(\d{1,2})\+ ans"
    m = re.search(r"\b(\d{1,2})\s*(?:\+\s*)?ans\b", text, flags=re.IGNORECASE)
    if m:
        try:
            return float(m.group(1))
        except Exception:
            pass
    return 0.0


def _extract_sections_list(text: str, section_titles: List[str]) -> List[str]:
    # Extrait grossier: prend les 800 premiers chars après un titre connu
    for title in section_titles:
        # ex: "Experience" / "Expérience" / "Expérience professionnelle"
        pattern = r"(?:^|\n)\s*" + re.escape(title) + r"\s*[:\-]?\s*\n"
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if not m:
            continue
        start = m.end()
        chunk = text[start : start + 800]
        # items possibles par lignes
        items = [i.strip() for i in re.split(r"\n|•|\-\s", chunk) if i.strip()]
        # nettoyer items trop courts
        items = [i for i in items if len(i) >= 6]
        return items[:10]
    return []


def _extract_education(text: str) -> List[str]:
    return _extract_sections_list(
        text,
        ["Education", "Educations", "Diplômes", "Diplome", "Formation", "Formations"],
    )


def _extract_experience(text: str) -> List[str]:
    return _extract_sections_list(
        text,
        [
            "Experience",
            "Expérience",
            "Expérience professionnelle",
            "Professional Experience",
            "Expérience",
        ],
    )


def _read_file_text(file_path: str) -> str:
    # PyPDF2 uniquement pour PDF; fallback texte si txt
    if file_path.lower().endswith(".pdf"):
        from PyPDF2 import PdfReader

        reader = PdfReader(file_path)
        pages = []
        for page in reader.pages:
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
        return "\n".join(pages)

    # txt / doc/docx: on limite au plus simple (doc/docx non supportés sans libs supplémentaires)
    # Pour compatibilité, si ce n'est pas pdf, on renvoie vide.
    if file_path.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    return ""


class CVAnalyzerRegex:
    def analyze_cv(self, file_path: str) -> Dict[str, Any]:
        raw_text = _read_file_text(file_path)
        processed_text = _collapse_whitespace(raw_text)

        emails = _extract_emails(processed_text)
        phones = _extract_phones(processed_text)

        skills = _extract_skills(processed_text)
        languages = _extract_languages(processed_text)

        education = _extract_education(processed_text)
        experience = _extract_experience(processed_text)

        years_experience = _extract_years_experience(processed_text)

        # Un résumé simple
        full_text = processed_text[:1200]

        return {
            "skills": skills,
            "education": education,
            "experience": experience,
            "languages": languages,
            "contact_info": {"emails": emails, "phones": phones},
            "years_experience": years_experience,
            "full_text": full_text,
            "processed_text": processed_text,
            "raw_text": raw_text,
        }


cv_analyzer = CVAnalyzerRegex()

