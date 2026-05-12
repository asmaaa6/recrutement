"""Matching CV ↔ Offre (TF-IDF + similarité cosinus)

Objectif:
- Construire un espace TF-IDF unique
- Calculer la similarité cosinus entre CV et offre

Sortie:
- classer_candidats(candidats, info_offre) -> liste triée avec score_global (0-1)
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _liste_securisee(valeur: Any) -> List[str]:
    if valeur is None:
        return []
    if isinstance(valeur, list):
        return [str(item) for item in valeur if item is not None]
    if isinstance(valeur, str):
        elements = [item.strip() for item in valeur.split(",")]
        return [item for item in elements if item]
    return [str(valeur)]


def _normaliser_texte(texte: str) -> str:
    texte = (texte or "").lower().strip()
    texte = re.sub(r"[^a-z0-9+\-\s]+", " ", texte)
    texte = re.sub(r"\s+", " ", texte)
    return texte


def _construire_texte_offre(info_offre: Dict[str, Any]) -> str:
    titre = info_offre.get("title") or ""
    description = info_offre.get("description") or ""
    competences_requises = " ".join(_liste_securisee(info_offre.get("required_skills")))
    competences_preferees = " ".join(_liste_securisee(info_offre.get("preferred_skills")))
    return _normaliser_texte(" ".join([titre, competences_requises, competences_preferees, description]))


def _construire_texte_cv(info_cv: Dict[str, Any]) -> str:
    competences = " ".join(_liste_securisee(info_cv.get("skills")))
    texte_traite = info_cv.get("processed_text") or ""
    texte_brut = info_cv.get("raw_text") or ""
    texte_complet = info_cv.get("full_text") or ""
    base = texte_traite or texte_brut or texte_complet or ""
    return _normaliser_texte(" ".join([competences, base]))


class CVMatcheurTfidfCosinus:
    def __init__(
        self,
        plage_ngrammes: tuple[int, int] = (1, 2),
        max_caracteres: int = 5000,
        min_df: int = 1,
    ):
        self.vehiculiseur = TfidfVectorizer(
            lowercase=True,
            ngram_range=plage_ngrammes,
            min_df=min_df,
            max_features=max_caracteres,
        )

    def score_correspondance(self, texte_cv: str, texte_offre: str) -> float:
        matrice = self.vehiculiseur.fit_transform([texte_cv, texte_offre])
        similarite = cosine_similarity(matrice[0], matrice[1])[0][0]
        similarite = max(0.0, min(1.0, float(similarite)))
        return similarite

    def classer_candidats(
        self,
        candidats: List[Dict[str, Any]],
        info_offre: Dict[str, Any],
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        texte_offre = _construire_texte_offre(info_offre)

        textes_cv = [_construire_texte_cv(c.get("cv_info", {})) for c in candidats]

        if not textes_cv:
            return []

        textes_tous = textes_cv + [texte_offre]
        matrice = self.vehiculiseur.fit_transform(textes_tous)

        vecteur_offre = matrice[-1]
        vecteurs_cv = matrice[:-1]
        similarities = cosine_similarity(vecteurs_cv, vecteur_offre).reshape(-1)

        resultats = []
        for index, candidat in enumerate(candidats):
            score = float(similarities[index])
            resultats.append(
                {
                    "candidate_id": candidat.get("id"),
                    "name": candidat.get("name"),
                    "global_score": score,
                    "textual_score": score,
                    "recommendation": self._obtenir_recommandation(score),
                }
            )

        resultats.sort(key=lambda item: item["global_score"], reverse=True)
        if top_k is not None:
            resultats = resultats[:top_k]
        return resultats

    @staticmethod
    def _obtenir_recommandation(score: float) -> str:
        if score >= 0.85:
            return "Excellente correspondance - À interviewer en priorité"
        if score >= 0.7:
            return "Bonne correspondance - Recommandé"
        if score >= 0.5:
            return "Correspondance acceptable - À considérer"
        return "Faible correspondance - Consulter manuellement"


cv_matcher = CVMatcheurTfidfCosinus()

