# Guide de Démarrage - RecrutAI

## 🚀 Lancer l'application

### Option 1: Lancement rapide (Sans base de données)

```bash
# 1. Accéder au dossier
cd /Users/asma/Desktop/recrutement

# 2. Créer un environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer l'application
python app.py
```

L'application sera disponible à: **http://localhost:5000**

### Option 2: Lancement complet (Avec MySQL)

#### Prérequis
- MySQL Server installé et en cours d'exécution
- Accès root ou compte administrateur MySQL

#### Étapes

1. **Créer la base de données**
```bash
mysql -u root -p < database/schema.sql
```

2. **Configurer la connexion MySQL**

   Éditer `config.py`:
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:votre_password@localhost:3306/recrutement'
   ```

3. **Télécharger les modèles spaCy**
```bash
python -m spacy download fr_core_news_sm
```

4. **Initialiser la base de données Flask**
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

5. **Lancer l'application**
```bash
python app.py
```

## 📍 URLs Importantes

| Route | Description |
|-------|-------------|
| `/` | Page d'accueil |
| `/login` | Connexion |
| `/signup` | Inscription |
| `/dashboard` | Tableau de bord candidat |
| `/recruiter-dashboard` | Tableau de bord recruteur |
| `/cv-upload` | Upload CV |
| `/cv-analysis` | Analyse CV |
| `/chatbot` | Chatbot d'aide |

## 🔧 Configuration

### Variables d'environnement (optionnel)

Créer un fichier `.env`:
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=votre-clé-secrète-très-sécurisée
DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3306/recrutement
```

### Modes d'exécution

**Mode Développement:**
```bash
export FLASK_ENV=development
python app.py
```

**Mode Production:**
```bash
export FLASK_ENV=production
gunicorn -w 4 app:app
```

## 🐛 Dépannage

### Erreur: `ModuleNotFoundError: No module named 'flask'`
```bash

pip install -r requirements.txt
```

### Erreur: `No module named 'spacy'`
```bash
pip install spacy
python -m spacy download fr_core_news_sm
```

### Erreur: `MySQL Connection Error`
1. Vérifier que MySQL est en cours d'exécution
2. Vérifier les identifiants dans `config.py`
3. Vérifier que la base de données existe

###  Erreur: `Port 5000 already in use`
```bash
# Changer le port dans app.py
python app.py --port 5001
```

## 📦 Dépendances Principales

- **Flask** - Framework web
- **Flask-SQLAlchemy** - ORM
- **Flask-Login** - Authentification
- **PyPDF2** - Lecture PDF
- **pdfminer** - Extraction texte PDF
- **scikit-learn** - Machine Learning
- **spaCy** - Traitement du langage naturel
- **Bootstrap 5** - Framework CSS

## 🧪 Tests

### Tester la page d'accueil
```
1. Aller à http://localhost:5000
2. Vérifier que le design s'affiche correctement
3. Cliquer sur les boutons de navigation
```

### Tester l'upload CV
```
1. Aller à /cv-upload
2. Déposer un fichier PDF
3. Vérifier que le fichier est accepté
```

### Tester le chatbot
```
1. Aller à /chatbot
2. Poser une question
3. Vérifier que le chatbot répond
```

## 📊 Structure de la Base de Données

```
users (id, username, email, role, ...)
├── cvs (id, user_id, file_path, ...)
├── applications (id, user_id, offer_id, ...)
│   └── offers (id, recruiter_id, ...)
└── conversations (id, user_id, message, ...)
```

## 🔐 Sécurité

> **⚠️ ATTENTION:** 
> - Ne JAMAIS commiter le fichier `.env`
> - Utiliser des mots de passe sécurisés
> - Changer `SECRET_KEY` en production
> - Utiliser HTTPS en production
> - Activer CORS uniquement si nécessaire

## 📚 Documentation Supplémentaire

- [README.md](README.md) - Vue d'ensemble du projet
- [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md) - Journal de développement
- [database/schema.sql](database/schema.sql) - Schéma base de données

## ⚙️ Maintenance

### Nettoyer la base de données
```bash
python
>>> from app import db
>>> db.drop_all()
>>> db.create_all()
```

### Générer les migrations
```bash
flask db init
flask db migrate
flask db upgrade
```

### Backuper la base de données
```bash
mysqldump -u root -p recrutement > backup.sql
```

## 🚀 Déploiement

### Avec Heroku
```bash
heroku create votre-app-name
git push heroku main
heroku addons:create cleardb:ignite
```

### Avec AWS
```bash
# Configurer EB CLI
eb init -p python-3.9 recrutement-app
eb create production
eb deploy
```

---

**Questions?** Consultez le README.md ou créez une issue GitHub!
