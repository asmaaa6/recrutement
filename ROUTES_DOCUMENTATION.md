# 🗺️ ROUTES DISPONIBLES - RecrutAI

## Routes Publiques (Sans Authentification)

### Accueil & Informations
```
GET  /                          → index.html (Page d'accueil)
GET  /login                     → login.html (Formulaire connexion)
GET  /signup                    → signup.html (Formulaire inscription)
POST /login                     → Traitement connexion
POST /signup                    → Traitement inscription
```

### Gestion des Erreurs
```
GET  /404                       → 404.html (Page non trouvée)
GET  /500                       → 500.html (Erreur serveur)
```

## Routes Protégées (Authentification Requise)

### Dashboard & Profil
```
GET  /dashboard                 → dashboard.html (Tableau de bord candidat)
GET  /recruiter-dashboard       → recruiter-dashboard.html (Tableau de bord recruteur)
GET  /profile                   → profile.html (Mon profil)
GET  /settings                  → Paramètres utilisateur
POST /profile                   → Mise à jour profil
POST /logout                    → Déconnexion
```

### CV (Candidats)
```
GET  /cv-upload                 → cv-upload.html (Page d'upload)
POST /cv-upload                 → Traitement upload CV
GET  /cv-analysis               → cv-analysis.html (Résultats analyse)
GET  /cv-history                → Historique des CV
DELETE /cv/{cv_id}              → Supprimer un CV
```

### Offres d'Emploi
```
GET  /offers                    → Liste les offres
GET  /offers/{offer_id}         → Détails d'une offre
GET  /offers/search             → Recherche offres avec filtres
POST /offers/apply              → Postuler à une offre
```

### Candidatures (Candidats)
```
GET  /applications              → Liste mes candidatures
GET  /applications/{app_id}     → Détails candidature
POST /applications/{app_id}/withdraw → Retirer candidature
PATCH /applications/{app_id}/status   → Mettre à jour statut
```

### Candidatures (Recruteurs)
```
GET  /recruiter/applications    → Toutes les candidatures reçues
GET  /recruiter/applications/{offer_id} → Candidatures par offre
PATCH /recruiter/applications/{app_id}/status → Changer statut candidature
POST /recruiter/applications/{app_id}/notes   → Ajouter des notes
```

### Offres (Recruteurs)
```
POST /recruiter/offers/create   → Créer une offre
GET  /recruiter/offers          → Mes offres
GET  /recruiter/offers/{offer_id}/edit → Editer une offre
PUT  /recruiter/offers/{offer_id}      → Mettre à jour offre
DELETE /recruiter/offers/{offer_id}    → Supprimer offre
GET  /recruiter/offers/{offer_id}/candidates → Top candidats
```

### Chatbot
```
GET  /chatbot                   → chatbot.html (Interface chat)
POST /api/chatbot/message       → Envoyer message
GET  /api/chatbot/history       → Historique conversations
DELETE /api/chatbot/{conv_id}   → Supprimer conversation
```

### Dashboard
```
GET  /dashboard/stats           → Statistiques
GET  /api/dashboard/candidate   → Stats candidat (JSON)
GET  /api/dashboard/recruiter   → Stats recruteur (JSON)
GET  /api/dashboard/admin       → Stats admin (JSON)
GET  /api/dashboard/export      → Exporter statistiques
```

### Admin
```
GET  /admin                     → Panel admin
GET  /admin/users               → Gestion utilisateurs
GET  /admin/offers              → Gestion offres
GET  /admin/applications        → Gestion candidatures
DELETE /admin/users/{user_id}   → Supprimer utilisateur
```

## Routes API REST

### Authentication API
```
POST   /api/auth/register       → Inscription
POST   /api/auth/login          → Connexion
POST   /api/auth/logout         → Déconnexion
POST   /api/auth/refresh        → Rafraîchir token
GET    /api/auth/me             → Infos utilisateur courant
```

### CVs API
```
POST   /api/cvs/upload          → Upload CV
GET    /api/cvs                 → Liste mes CVs
GET    /api/cvs/{cv_id}         → Détails CV
GET    /api/cvs/{cv_id}/analysis → Résultats analyse
DELETE /api/cvs/{cv_id}         → Supprimer CV
```

### Offers API
```
GET    /api/offers              → Liste les offres (paginated)
POST   /api/offers              → Créer offre (Recruteur)
GET    /api/offers/{offer_id}   → Détails offre
PUT    /api/offers/{offer_id}   → Modifier offre
DELETE /api/offers/{offer_id}   → Supprimer offre
GET    /api/offers/search       → Recherche avec filtres
```

### Applications API
```
POST   /api/applications        → Postuler
GET    /api/applications        → Mes candidatures
GET    /api/applications/{app_id} → Détails candidature
PATCH  /api/applications/{app_id}/status → Changer statut
DELETE /api/applications/{app_id} → Retirer candidature
GET    /api/offers/{offer_id}/applications → Apps pour une offre
```

### Matching API
```
GET    /api/matching/{cv_id}/offer/{offer_id} → Score matching
GET    /api/offers/{offer_id}/top-candidates  → Top candidats
GET    /api/matching/stats                    → Stats matching
```

### Chatbot API
```
POST   /api/chatbot/message     → Envoyer message
GET    /api/chatbot/conversations/{id} → Historique
DELETE /api/chatbot/conversations/{id} → Supprimer conversation
```

### Dashboard API
```
GET    /api/dashboard/candidate → Stats candidat
GET    /api/dashboard/recruiter → Stats recruteur
GET    /api/dashboard/admin     → Stats admin
GET    /api/dashboard/export    → Exportation (CSV/PDF)
```

## Codes de Réponse HTTP

```
✅ 200  OK                  - Requête réussie
✅ 201  Created             - Ressource créée
✅ 204  No Content          - Succès (aucun contenu)
❌ 400  Bad Request         - Données invalides
❌ 401  Unauthorized        - Authentification requise
❌ 403  Forbidden           - Permission refusée
❌ 404  Not Found           - Ressource non trouvée
❌ 409  Conflict            - Conflit (ex: email déjà utilisé)
❌ 500  Server Error        - Erreur serveur
```

## Méthodes HTTP Utilisées

```
GET     → Récupérer une ressource
POST    → Créer une ressource
PUT     → Remplacer une ressource
PATCH   → Modifier partiellement
DELETE  → Supprimer une ressource
```

## Authentification

### Headers Requis
```
Authorization: Bearer {token}
Content-Type: application/json
```

### Tokens JWT
- Format: `Bearer {eyJhbGciOiJIUzI1NiIs...}`
- Expiration: 7 jours par défaut
- Refresh: GET `/api/auth/refresh`

## Paramètres Courants

### Pagination
```
?page=1&limit=20
```

### Filtrage
```
?status=pending
?job_type=CDI
?min_salary=40000&max_salary=60000
?search=terme
```

### Tri
```
?sort=created_at&order=desc
?sort=match_score&order=asc
```

## Formats de Réponse

### Succès
```json
{
  "status": "success",
  "data": { ... },
  "message": "Operation completed"
}
```

### Erreur
```json
{
  "status": "error",
  "code": "INVALID_REQUEST",
  "message": "Description de l'erreur",
  "errors": [
    { "field": "email", "message": "Email invalide" }
  ]
}
```

## Webhooks (Future)

```
POST https://votre-domain.com/webhooks/application
POST https://votre-domain.com/webhooks/offer
POST https://votre-domain.com/webhooks/cv_analysis
```

## Rate Limiting

```
General:    100 req/minute
Auth:       5 req/minute (login)
Upload:     10 req/minute
Matching:   50 req/minute
```

## CORS

Autorisés pour:
```
http://localhost:3000
http://localhost:5000
https://recrutai.com
```

## Exemples de Requêtes cURL

### Upload CV
```bash
curl -X POST http://localhost:5000/api/cvs/upload \
  -H "Authorization: Bearer {token}" \
  -F "file=@resume.pdf"
```

### Postuler à une offre
```bash
curl -X POST http://localhost:5000/api/applications \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "offer_id": 1,
    "cv_id": 1,
    "message": "Je suis intéressé"
  }'
```

### Obtenir le score de matching
```bash
curl -X GET "http://localhost:5000/api/matching/1/offer/1" \
  -H "Authorization: Bearer {token}"
```

### Recherche d'offres
```bash
curl -X GET "http://localhost:5000/api/offers?job_type=CDI&min_salary=40000" \
  -H "Authorization: Bearer {token}"
```

### Envoyer message chatbot
```bash
curl -X POST http://localhost:5000/api/chatbot/message \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quel est le processus?"
  }'
```

## Statuts Possibles

### Candidatures
- `pending` - En attente d'examen
- `under_review` - En cours de révision
- `shortlisted` - Raccourci
- `accepted` - Acceptée
- `rejected` - Rejetée
- `withdrawn` - Retirée

### Offres
- `open` - Ouverte
- `closed` - Fermée
- `filled` - Pourvue

### Utilisateurs
- `active` - Actif
- `inactive` - Inactif
- `banned` - Banní

---

**Documentation**: Mise à jour: 29 Mars 2026
