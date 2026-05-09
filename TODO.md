# TODO - Refactor Flask RecrutAI

## Étape 1 — Réécriture backend (routes + blueprints)
- [x] Réécrire `app.py` pour utiliser les blueprints `modules.auth` et `modules.applications`

- [ ] Ajouter/brancher la route `/chatbot`

## Étape 2 — Auth complète
- [x] Réécrire `modules/auth.py` (register + login complets) sans `pass`


## Étape 3 — Upload CV côté recruteur
- [x] Réécrire `modules/applications.py` sans `pass`

- [ ] Route `/cv-upload` fonctionnelle : upload par recruteur seulement

## Étape 4 — Analyse CV par regex uniquement
- [x] Réécrire `modules/cv_analysis.py` : regex uniquement (PyPDF2 + regex)


## Étape 5 — Matching TF-IDF + cosinus
- [x] Réécrire `modules/matching.py` en TF-IDF + similarité cosinus


## Étape 6 — Chatbot réponses prédéfinies
- [x] Réécrire `modules/chatbot.py` : réponses simples prédéfinies


## Étape 7 — Tests
- [ ] Lancer l’app et tester : `/signup`, `/login`, `/dashboard`, `/cv-upload`, `/chatbot`


