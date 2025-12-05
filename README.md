# BdF Demo IA - Carnet d'Adresses v2.1

Application FastAPI avec **architecture modulaire** pour gérer un carnet d'adresses de personnes, de projets informatiques et de **tâches**.

## ✨ Nouveauté v2.1 - Gestion des Tâches

La version 2.1 ajoute un système complet de **gestion des tâches** permettant de :
- ✅ Créer des tâches liées à des projets
- 👤 Assigner des tâches à des personnes
- 📅 Définir des dates de début et fin
- 🔍 Filtrer les tâches (par projet, personne, dates)
- 📊 Visualiser les tâches actives

**📖 [Guide complet des tâches →](GUIDE_TACHES.md)**

## 🏗️ Architecture v2.1 - Modulaire et Scalable

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

2. Configurer les variables d'environnement :
```bash
# Copier le template de configuration
cp .env.example .env

# Éditer .env si nécessaire (les valeurs par défaut fonctionnent avec run_postgres.sh)
nano .env
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Pour le développement et les tests :
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

### Person (Personne)
- **last_name** (obligatoire)
- **first_name** (obligatoire)
- Le couple last_name/first_name doit être unique
- client
- client_city
- position
- personal_email
- professional_email
- landline_phone
- mobile
- team
- manager
- profile_id (référence vers Profile)

### Project (Projet)
- **name** (obligatoire)
- description
- **lead_developer_id** (obligatoire, référence vers Person)
- project_manager_id (optionnel, référence vers Person)
- dev_line_id (optionnel, référence vers Person)
- category_id (optionnel, référence vers Category)

### Task (Tâche) 🆕
- **title** (obligatoire)
- description
- **start_date** (obligatoire)
- **end_date** (obligatoire)
- **project_id** (obligatoire, référence vers Project)
- **assigned_person_id** (obligatoire, référence vers Person)

### Category (Catégorie)
- **name** (obligatoire)
- description

### Profile (Profil)
- **name** (obligatoire)
- description

## Endpoints API (v1)

Tous les endpoints sont préfixés par `/api/v1`

### Persons (Personnes)
- `POST /api/v1/persons/` - Créer une personne
- `GET /api/v1/persons/` - Lister toutes les personnes
- `GET /api/v1/persons/{id}` - Récupérer une personne
- `GET /api/v1/persons/by-profile/{profile_id}` - Personnes par profil
- `PUT /api/v1/persons/{id}` - Mettre à jour une personne
- `DELETE /api/v1/persons/{id}` - Supprimer une personne

### Projects (Projets)
- `POST /api/v1/projects/` - Créer un projet
- `GET /api/v1/projects/` - Lister tous les projets
- `GET /api/v1/projects/{id}` - Récupérer un projet
- `GET /api/v1/projects/by-category/{category_id}` - Projets par catégorie
- `PUT /api/v1/projects/{id}` - Mettre à jour un projet
- `DELETE /api/v1/projects/{id}` - Supprimer un projet

### Tasks (Tâches) 🆕
- `POST /api/v1/tasks/` - Créer une tâche
- `GET /api/v1/tasks/` - Lister toutes les tâches
- `GET /api/v1/tasks/{id}` - Récupérer une tâche
- `GET /api/v1/tasks/by-project/{project_id}` - Tâches d'un projet
- `GET /api/v1/tasks/by-person/{person_id}` - Tâches d'une personne
- `GET /api/v1/tasks/active/` - Tâches actives
- `PUT /api/v1/tasks/{id}` - Mettre à jour une tâche
- `DELETE /api/v1/tasks/{id}` - Supprimer une tâche

### Categories (Catégories)
- `POST /api/v1/categories/` - Créer une catégorie
- `GET /api/v1/categories/` - Lister toutes les catégories
- `GET /api/v1/categories/{id}` - Récupérer une catégorie
- `PUT /api/v1/categories/{id}` - Mettre à jour une catégorie
- `DELETE /api/v1/categories/{id}` - Supprimer une catégorie

### Profiles (Profils)
- `POST /api/v1/profiles/` - Créer un profil
- `GET /api/v1/profiles/` - Lister tous les profils
- `GET /api/v1/profiles/{id}` - Récupérer un profil
- `PUT /api/v1/profiles/{id}` - Mettre à jour un profil
- `DELETE /api/v1/profiles/{id}` - Supprimer un profil

## Tests

Exécuter tous les tests :
```bash
./scripts/run_tests.sh
```

Exécuter les tests avec couverture :
```bash
./scripts/run_tests.sh --cov=src --cov-report=html
```

Tests spécifiques :
```bash
./scripts/run_tests.sh tests/test_tasks.py -v
```

**Résultats actuels** : ✅ 37/37 tests passent (88% de couverture)

Les tests utilisent une base de données SQLite en mémoire pour ne pas affecter la base PostgreSQL.

## Exemples d'utilisation

### Démarrage rapide avec données de test

Peupler la base avec des données complètes (personnes, projets, tâches) :
```bash
# 1. Réinitialiser la base
./scripts/reset_database.sh

# 2. Lancer l'application
./scripts/run_app.sh &

# 3. Attendre que l'app démarre (2-3 secondes)
sleep 3

# 4. Peupler avec des données de test
./scripts/seed_with_tasks.sh
```

### Créer une personne

```bash
curl -X POST "http://localhost:8000/api/v1/persons/" \
  -H "Content-Type: application/json" \
  -d '{
    "last_name": "Dupont",
    "first_name": "Jean",
    "position": "Développeur",
    "professional_email": "jean.dupont@bdf.fr"
  }'
```

### Créer un projet

```bash
curl -X POST "http://localhost:8000/api/v1/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API de Gestion",
    "description": "API REST pour la gestion des ressources",
    "lead_developer_id": 1
  }'
```

### Créer une tâche 🆕

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Développer endpoint authentification",
    "description": "Implémenter JWT et OAuth2",
    "start_date": "2025-12-05",
    "end_date": "2025-12-15",
    "project_id": 1,
    "assigned_person_id": 1
  }'
```

### Lister les tâches actives

```bash
curl "http://localhost:8000/api/v1/tasks/active/"
```

**📖 Plus d'exemples dans [GUIDE_TACHES.md](GUIDE_TACHES.md)**
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

