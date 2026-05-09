"""Matching CV ↔ Offre (TF-IDF + similarité cosinus)

Objectif:
- Construire un vecteur TF-IDF (un seul espace)
- Calculer la similarité cosinus entre CV et Offre

On évite les mélanges ad-hoc: score = cosinus(CV_text, offer_text).

Sortie:
- rank_candidates(candidates, offer_info) -> liste triée avec global_score (0-1)
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _safe_list(x: Any) -> List[str]:
    if x is None:
        return []
    if isinstance(x, list):
        return [str(i) for i in x if i is not None]
    if isinstance(x, str):
        parts = [p.strip() for p in x.split(",")]
        return [p for p in parts if p]
    return [str(x)]


def _normalize_text(t: str) -> str:
    t = (t or "").lower().strip()
    t = re.sub(r"[^a-z0-9+\-\s]+", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t


def _build_offer_text(offer_info: Dict[str, Any]) -> str:
    title = offer_info.get("title") or ""
    desc = offer_info.get("description") or ""
    required = " ".join(_safe_list(offer_info.get("required_skills")))
    preferred = " ".join(_safe_list(offer_info.get("preferred_skills")))
    return _normalize_text(" ".join([title, required, preferred, desc]))


def _build_cv_text(cv_info: Dict[str, Any]) -> str:
    skills = " ".join(_safe_list(cv_info.get("skills")))
    processed = cv_info.get("processed_text") or ""
    raw = cv_info.get("raw_text") or ""
    full = cv_info.get("full_text") or ""
    base = processed or raw or full or ""
    return _normalize_text(" ".join([skills, base]))


class CVMatcherTfidfCosine:
    def __init__(
        self,
        ngram_range: tuple[int, int] = (1, 2),
        max_features: int = 5000,
        min_df: int = 1,
    ):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=ngram_range,
            min_df=min_df,
            max_features=max_features,
        )

    def match_score(self, cv_text: str, offer_text: str) -> float:
        X = self.vectorizer.fit_transform([cv_text, offer_text])
        sim = cosine_similarity(X[0], X[1])[0][0]  # 0..1
        if sim < 0:
            sim = 0.0
        if sim > 1:
            sim = 1.0
        return float(sim)

    def rank_candidates(
        self,
        candidates: List[Dict[str, Any]],
        offer_info: Dict[str, Any],
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        offer_text = _build_offer_text(offer_info)

        cv_texts = []
        for c in candidates:
            cv_texts.append(_build_cv_text(c.get("cv_info", {})))

        if not cv_texts:
            return []

        # Fit une fois sur tous les CV + l'offre
        all_texts = cv_texts + [offer_text]
        X = self.vectorizer.fit_transform(all_texts)

        # Similarité: chaque CV vs offer (dernier index)
        offer_vec = X[-1]
        cv_vecs = X[:-1]
        sims = cosine_similarity(cv_vecs, offer_vec).reshape(-1)

        results = []
        for i, c in enumerate(candidates):
            sim = float(sims[i])
            results.append(
                {
                    "candidate_id": c.get("id"),
                    "name": c.get("name"),
                    "global_score": sim,
                    "textual_score": sim,
                    "recommendation": self._get_recommendation(sim),
                }
            )

        results.sort(key=lambda x: x["global_score"], reverse=True)
        if top_k is not None:
            results = results[:top_k]
        return results

    @staticmethod
    def _get_recommendation(score: float) -> str:
        if score >= 0.85:
            return "Excellente correspondance - À interviewer en priorité"
        if score >= 0.7:
            return "Bonne correspondance - Recommandé"
        if score >= 0.5:
            return "Correspondance acceptable - À considérer"
        return "Faible correspondance - Consulter manuellement"


cv_matcher = CVMatcherTfidfCosine()

