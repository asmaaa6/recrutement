# 🧪 GUIDE DE TEST - RecrutAI

## Test de la Page d'Accueil

### Via le navigateur
```
1. Aller à http://localhost:5000
2. Vérifier que la page charge correctement
3. Tester tous les éléments :
   - Navigation bar sticky
   - Scroll smooth vers les sections
   - Animations des cartes au scroll
   - Boutons CTA cliquables
   - Responsive design (redimensionner la fenêtre)
```

### Couleurs & Design
- ✅ Vérifier que les couleurs pastel s'affichent
- ✅ Vérifier que les gradients sont fluides
- ✅ Vérifier que les animations fonctionnent
- ✅ Vérifier que les icônes s'affichent

## Test des Formulaires

### Inscription
```
1. Cliquer sur "Inscription" ou "Créer un compte"
2. Remplir le formulaire :
   - Nom d'utilisateur
   - Email
   - Rôle (Candidat/Recruteur)
   - Mot de passe
   - Confirmer mot de passe
3. Accepter les conditions
4. Cliquer "S'inscrire"
```

### Connexion
```
1. Cliquer sur "Connexion"
2. Entrer email et mot de passe
3. Cliquer "Connexion"
4. Vérifier la redirection vers le dashboard
```

## Test des Modules

### Module Authentification
```
✅ Formulaire inscription
✅ Formulaire connexion
✅ Déconnexion
✅ Profil utilisateur
✅ Rôles multimodaux
```

### Module Offres
```
✅ Voir la liste des offres
✅ Accéder au détail d'une offre
✅ Voir les candidatures (pour recruteur)
```

### Module Candidatures
```
✅ Voir mes candidatures
✅ Détails d'une candidature
✅ Statut candidature
```

### Module CV
```
✅ Upload CV (drag & drop)
✅ Voir l'analyse CV
✅ Voir les compétences détectées
✅ Voir le score de qualité
```

### Module Chatbot
```
✅ Ouvrir l'interface chatbot
✅ Envoyer un message
✅ Recevoir une réponse
✅ Historique des messages
```

### Module Dashboard
```
✅ Voir les statistiques
✅ Voir les cartes de statuts
✅ Voir les actions rapides
```

## Tests de Performance

### Temps de chargement
```
Page d'accueil:     < 2 secondes
Login/Signup:       < 1 seconde
Dashboard:          < 1.5 secondes
Upload CV:          Dépend du fichier
```

### Responsive Design
```
📱 Mobile (480px)
📱 Tablet (768px)
🖥️  Desktop (1024px+)
🖥️  Large Desktop (1600px+)
```

## Tests de Sécurité

### Authentification
```
✅ Mots de passe hachés
✅ Sessions sécurisées
✅ Protection CSRF
✅ Validation d'entrées
```

### Rôles
```
✅ Candidat → Accès dashboard candidat
✅ Recruteur → Accès recruiter-dashboard
✅ Admin → Accès panel admin
```

## Tests d'Intégration

### Database
```
1. Vérifier que la base de données se crée
2. Vérifier que les tables sont créées
3. Vérifier que les relations fonctionnent
4. Vérifier que les indexes existent
```

### API
```
1. Tester les endpoints avec Postman/cURL
2. Vérifier les codes de réponse HTTP
3. Vérifier les messages d'erreur
4. Vérifier les authentifications
```

## Checklist de Tout Fonctionne

### Frontend
- [ ] Page d'accueil s'affiche correctement
- [ ] Design pastel visible
- [ ] Animations fluides
- [ ] Responsive design fonctionne
- [ ] Navigation fonctionne
- [ ] Tous les liens fonctionnent
- [ ] Formulaires se valident

### Backend
- [ ] Application démarre sans erreur
- [ ] Routes répondent (200 OK)
- [ ] Base de données se connecte
- [ ] Modèles ORM fonctionnent
- [ ] Modules s'importent correctement

### Modules
- [ ] Auth module fonctionne
- [ ] CV module fonctionne
- [ ] Offers module fonctionne
- [ ] Applications module fonctionne
- [ ] Matching module fonctionne
- [ ] Chatbot module fonctionne
- [ ] Dashboard module fonctionne

### Design
- [ ] Couleurs pastel correctes
- [ ] Fonts correctes
- [ ] Icons s'affichent
- [ ] Spacing correct
- [ ] Alignements correct
- [ ] Aucun texte coupé
- [ ] Aucun débordement

## Tests Utilisateur

### Scénario 1: Candidat
```
1. S'inscrire comme candidat
2. Compléter le profil
3. Upload un CV
4. Voir l'analyse du CV
5. Voir les offres disponibles
6. Postuler à une offre
7. Utiliser le chatbot
8. Voir le statut de candidature
```

### Scénario 2: Recruteur
```
1. S'inscrire comme recruteur
2. Créer une offre d'emploi
3. Voir les candidatures
4. Voir le top des candidats
5. Utiliser le chatbot
6. Voir les statistiques
```

### Scénario 3: Admin
```
1. S'inscrire comme admin
2. Accéder au panel admin
3. Voir tous les utilisateurs
4. Voir toutes les offres
5. Voir toutes les candidatures
6. Voir les statistiques globales
```

## Tests de Charge

### Avec Apache Bench
```bash
ab -n 1000 -c 10 http://localhost:5000/
```

### Avec Locust
```bash
locust -f locustfile.py
```

## Debugging

### Activer les logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Vérifier la base de données
```bash
mysql -u root -p recrutement
SELECT * FROM users;
SELECT * FROM offers;
```

### Vérifier les imports
```bash
python -c "from modules import *"
```

## Problèmes Courants & Solutions

### Port 5000 déjà utilisé
```bash
# Changer le port dans app.py
python app.py --port 5001
```

### Module non trouvé
```bash
# Réinstaller les dépendances
pip install -r requirements.txt
```

### Base de données non accessible
```bash
# Vérifier que MySQL est en cours d'exécution
mysql -u root -p
```

### CSS/JS non chargé
```bash
# Vider le cache du navigateur
Ctrl+Shift+Delete (Chrome)
Cmd+Shift+Delete (Firefox)
```

## Déploiement Test

### Avec Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 app:app
```

### Avec Docker
```bash
docker build -t recrutai .
docker run -p 5000:5000 recrutai
```

---

**Préparé le**: 29 Mars 2026
