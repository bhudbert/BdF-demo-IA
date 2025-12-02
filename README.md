# BdF Demo IA - Carnet d'Adresses v2.0

Application FastAPI avec **architecture modulaire** pour gérer un carnet d'adresses de personnes et de projets informatiques.

## 🏗️ Architecture v2.0 - Modulaire et Scalable

Le projet utilise une architecture en couches avec le **Repository Pattern** pour une meilleure séparation des responsabilités.

```
src/
├── api/              # Couche API (endpoints, schémas)
├── core/             # Configuration
├── db/               # Base de données
├── models/           # Modèles de domaine
├── repositories/     # Accès aux données (CRUD)
└── main.py          # Point d'entrée
```

📖 **[Voir l'architecture détaillée →](ARCHITECTURE.md)**

## Prérequis

- Python 3.14
- Podman
- PostgreSQL 16 (via conteneur)

## Installation

1. Créer et activer l'environnement virtuel :
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Pour le développement et les tests :
```bash
pip install -r requirements-dev.txt
```

## Démarrage de la base de données

Lancer PostgreSQL avec Podman :
```bash
bash scripts/run_postgres.sh
```

La base de données sera accessible sur :
- Host: localhost
- Port: 5434
- Database: bdf_demo
- User: postgres
- Password: postgres

## Lancement de l'application

```bash
bash scripts/run_app.sh
```

Ou manuellement :
```bash
source .venv/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur http://localhost:8000

Documentation interactive :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

## Structure du projet

```
.
├── src/                    # Code source de l'application
│   ├── api/               # 🌐 Couche API
│   │   ├── routers/       # Endpoints REST
│   │   └── schemas.py     # Validation Pydantic
│   ├── core/              # ⚙️ Configuration
│   │   └── config.py      # Settings
│   ├── db/                # 💾 Base de données
│   │   ├── session.py     # SQLAlchemy
│   │   └── base.py        # Base + imports
│   ├── models/            # 📊 Modèles ORM
│   │   ├── personne.py
│   │   └── projet.py
│   ├── repositories/      # 🗄️ Accès données (CRUD)
│   │   ├── base_repository.py
│   │   ├── personne_repository.py
│   │   └── projet_repository.py
│   └── main.py           # Point d'entrée FastAPI
├── tests/                 # Tests unitaires
├── scripts/               # Scripts utilitaires
├── requirements.txt       # Dépendances de production
└── requirements-dev.txt   # Dépendances de développement
```

## Modèles de données

### Personne
- **nom** (obligatoire)
- **prenom** (obligatoire)
- Le couple nom/prenom doit être unique
- client
- ville_client
- fonction
- email_perso
- email_pro
- telephone_fixe
- mobile
- equipe
- responsable

### Projet
- **nom** (obligatoire)
- description
- **developpeur_principal** (obligatoire, référence vers Personne)
- chef_projet (optionnel, référence vers Personne)
- ligne_de_dev (optionnel, référence vers Personne)

## Endpoints API

### Personnes

- `POST /personnes/` - Créer une personne
- `GET /personnes/` - Lister toutes les personnes
- `GET /personnes/{id}` - Récupérer une personne
- `PUT /personnes/{id}` - Mettre à jour une personne
- `DELETE /personnes/{id}` - Supprimer une personne

### Projets

- `POST /projets/` - Créer un projet
- `GET /projets/` - Lister tous les projets
- `GET /projets/{id}` - Récupérer un projet
- `PUT /projets/{id}` - Mettre à jour un projet
- `DELETE /projets/{id}` - Supprimer un projet

## Tests

Exécuter tous les tests :
```bash
source .venv/bin/activate
export PYTHONPATH=$PWD:$PYTHONPATH
pytest tests/ -v
```

Exécuter les tests avec couverture :
```bash
pytest tests/ --cov=src --cov-report=html
```

Les tests utilisent une base de données SQLite en mémoire pour ne pas affecter la base PostgreSQL.

## Exemples d'utilisation

### Créer une personne

```bash
curl -X POST "http://localhost:8000/personnes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Dupont",
    "prenom": "Jean",
    "fonction": "Développeur",
    "email_pro": "jean.dupont@bdf.fr"
  }'
```

### Créer un projet

```bash
curl -X POST "http://localhost:8000/projets/" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Projet Alpha",
    "description": "Description du projet",
    "developpeur_principal_id": 1
  }'
```

## Technologies utilisées

- **FastAPI** - Framework web moderne et rapide
- **SQLAlchemy** - ORM pour Python
- **Pydantic** - Validation des données
- **PostgreSQL** - Base de données relationnelle
- **psycopg** - Adaptateur PostgreSQL pour Python
- **pytest** - Framework de tests
- **Uvicorn** - Serveur ASGI

## Prochaines étapes suggérées

1. **Migrations de base de données** : Intégrer Alembic pour gérer les migrations
2. **Authentification** : Ajouter JWT/OAuth2 pour sécuriser l'API
3. **Filtres avancés** : Permettre la recherche et le filtrage des données
4. **Pagination** : Améliorer la pagination avec des métadonnées
5. **Validation avancée** : Ajouter des validations personnalisées (format email, téléphone, etc.)
6. **Logging** : Mettre en place un système de logs structuré
7. **Conteneurisation** : Créer un Dockerfile pour l'application
8. **CI/CD** : Mettre en place des pipelines d'intégration continue

## Licence

Ce projet est un démonstrateur pour la Banque de France.

