# RecrutAI - Plateforme de Recrutement par IA

Une plateforme web intelligente et moderne pour le recrutement basée sur l'intelligence artificielle.

## 🎯 Fonctionnalités Principales

✅ **Analyse Automatique de CV** - Extraction intelligente des informations (compétences, diplômes, expérience)
✅ **Matching Intelligent** - Compatibilité automatique entre CV et offres d'emploi
✅ **Chatbot Conversationnel** - Assistant IA pour les candidats et recruteurs
✅ **Tableau de Bord** - Statistiques et métriques en temps réel
✅ **Gestion Multi-Rôles** - Interfaces adaptées (candidat, recruteur, admin)
✅ **Sécurité Renforcée** - Authentification, cryptage et respect RGPD

## 🏗️ Architecture

```
recrutement/
├── app.py                 # Application Flask principale
├── config.py              # Configuration
├── requirements.txt       # Dépendances
├── static/                # Fichiers statiques (CSS, JS, Images)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   └── chatbot.js
│   └── images/
├── templates/             # Templates HTML
│   ├── index.html         # Page d'accueil
│   ├── login.html         # Connexion
│   ├── signup.html        # Inscription
│   ├── dashboard.html     # Tableau de bord candidat
│   ├── recruiter-dashboard.html  # Tableau de bord recruteur
│   ├── cv-upload.html     # Upload CV
│   ├── cv-analysis.html   # Analyse CV
│   └── chatbot.html       # Interface chatbot
├── modules/               # Modules métier
│   ├── auth.py            # Authentification
│   ├── offers.py          # Gestion des offres
│   ├── applications.py    # Gestion des candidatures
│   ├── cv_analysis.py     # Analyse CV (IA)
│   ├── matching.py        # Matching CV-Offre
│   ├── chatbot.py         # Chatbot
│   └── dashboard.py       # Dashboard
├── models/                # Modèles de données
│   ├── user.py            # Modèle Utilisateur
│   ├── offer.py           # Modèle Offre
│   ├── application.py     # Modèle Candidature
│   └── cv.py              # Modèle CV
├── utils/                 # Utilitaires
│   ├── pdf_extractor.py   # Extraction PDF
│   ├── text_processor.py  # Traitement texte
│   └── score_calculator.py # Calcul de scores
└── database/
    └── schema.sql         # Schéma MySQL
```

## 💻 Stack Technologique

| Couche | Technologie | Details |
|--------|-------------|---------|
| **Frontend** | HTML5, CSS3, JavaScript | Bootstrap 5, Design Pastel |
| **Backend** | Python | Flask 3.0 |
| **Base de Données** | MySQL | SQLAlchemy ORM |
| **IA/ML** | Scikit-learn, spaCy | Matching, analyse texte |
| **PDF** | PyPDF2, pdfminer | Extraction de texte |
| **Authentification** | Flask-Login | Gestion des sessions |

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone <repo-url>
cd recrutement
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur macOS/Linux
# ou
venv\Scripts\activate     # Sur Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Télécharger le modèle spaCy
```bash
python -m spacy download fr_core_news_sm
```

### 5. Configurer la base de données

Modifiez le fichier `config.py` avec vos données MySQL :
```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:password@localhost:3306/recrutement'
```

Puis exécutez le schéma :
```bash
mysql -u root -p recrutement < database/schema.sql
```

### 6. Lancer l'application
```bash
python app.py
```

L'application sera disponible à `http://localhost:5000`

## 📊 Modules Implémentés

### A. Module Authentification ✅
- Inscription de nouveaux utilisateurs
- Connexion sécurisée
- Gestion des rôles (Admin/Recruteur/Candidat)

### B. Module Gestion des Offres ✅
- Créer/Modifier/Supprimer des offres
- Consulter les candidatures par offre
- Statut des offres (ouverte/fermée/pourvue)

### C. Module Gestion des Candidatures ✅
- Upload de CV
- Consultation des candidatures
- Suivi des candidats

### D. Module Analyse CV ✅
- Extraction de texte (PDF, DOC, TXT)
- Détection des compétences
- Détection des diplômes
- Détection des expériences

### E. Module Matching ✅
- Comparaison CV-Offre
- Calcul du score de compatibilité
- Classement des candidats par score

### F. Module Chatbot ✅
- Réponses aux questions des candidats
- Discussions conversationnelles
- Stockage des conversations

### G. Module Dashboard ✅
- Statistiques en temps réel
- Classement des candidats
- Détails des candidatures

## 🎨 Design & Ergonomie

La plateforme utilise un **design pastel moderne** avec les couleurs suivantes:
- 🔵 Bleu Pastel: `#B4D7FF`
- 🩷 Rose Pastel: `#FFB6D9`
- 💚 Vert Pastel: `#B8E6D5`
- 💜 Purple Pastel: `#D4C4E8`
- 💛 Jaune Pastel: `#FFE5A1`

## 📝 Plans Futurs

- [ ] Intégration d'un modèle de Deep Learning avancé
- [ ] Système de recommandations personnalisé
- [ ] Vidéo interview enregistrée
- [ ] Intégration Slack/MS Teams
- [ ] Rapports PDF automatiques
- [ ] Système de scoring avancé

## 🔒 Sécurité

- Authentification Flask-Login
- Hachage sécurisé des mots de passe (werkzeug)
- Validation des entrées
- Protection CSRF avec Flask-WTF
- Respect du RGPD

## 📧 Support

Pour toute question ou bug report :
- Email: info@recrutai.com
- Issues: [GitHub Issues]

## 📄 Licence

Projet académique - Université [À compléter]

## 👥 Contributeurs

- [Votre nom]
- Équipe pédagogique

---

**v1.0** - Créé le 29 Mars 2026
