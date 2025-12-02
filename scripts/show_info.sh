#!/usr/bin/env bash
# Script de démonstration rapide du projet

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║          BdF Demo IA - Carnet d'Adresses                     ║
║          Projet FastAPI + PostgreSQL                         ║
╚══════════════════════════════════════════════════════════════╝

📋 RÉSUMÉ DU PROJET
──────────────────────────────────────────────────────────────

✅ Application FastAPI complète
✅ Connexion PostgreSQL 16 (Podman)
✅ Modèles : Personne et Projet
✅ CRUD complet pour les deux entités
✅ 17 tests unitaires (pytest)
✅ Documentation interactive Swagger/ReDoc

📁 STRUCTURE
──────────────────────────────────────────────────────────────

BdF-demo-IA/
├── src/                    Code source de l'application
│   ├── config.py          Configuration DB
│   ├── database.py        SQLAlchemy setup
│   ├── models.py          Modèles ORM
│   ├── schemas.py         Schémas Pydantic
│   ├── crud.py            Opérations CRUD
│   ├── main.py            Application FastAPI
│   └── routers/           Routes API
├── tests/                 Tests unitaires (17 tests)
├── scripts/               Scripts utilitaires
├── requirements.txt       Dépendances production
└── requirements-dev.txt   Dépendances dev/tests

🚀 DÉMARRAGE RAPIDE
──────────────────────────────────────────────────────────────

1. Activer l'environnement virtuel :
   $ source .venv/bin/activate

2. Lancer PostgreSQL :
   $ bash scripts/run_postgres.sh

3. Lancer l'application :
   $ bash scripts/run_app.sh
   # ou manuellement :
   $ uvicorn src.main:app --reload

4. Ouvrir la documentation :
   👉 http://localhost:8000/docs

🧪 TESTS
──────────────────────────────────────────────────────────────

Exécuter tous les tests :
$ bash scripts/run_tests.sh

Ou manuellement :
$ export PYTHONPATH=$PWD
$ pytest tests/ -v

Tests disponibles :
✓ test_main.py         (2 tests)  - Tests de l'API principale
✓ test_personnes.py    (9 tests)  - Tests CRUD Personnes
✓ test_projets.py      (8 tests)  - Tests CRUD Projets

📊 ENDPOINTS API
──────────────────────────────────────────────────────────────

Documentation :
  GET  /                 Endpoint racine
  GET  /health           Health check
  GET  /docs             Swagger UI
  GET  /redoc            ReDoc

Personnes :
  POST   /personnes/     Créer une personne
  GET    /personnes/     Lister les personnes
  GET    /personnes/{id} Récupérer une personne
  PUT    /personnes/{id} Modifier une personne
  DELETE /personnes/{id} Supprimer une personne

Projets :
  POST   /projets/       Créer un projet
  GET    /projets/       Lister les projets
  GET    /projets/{id}   Récupérer un projet
  PUT    /projets/{id}   Modifier un projet
  DELETE /projets/{id}   Supprimer un projet

💾 BASE DE DONNÉES
──────────────────────────────────────────────────────────────

PostgreSQL 16 (via Podman) :
  Host     : localhost
  Port     : 5434
  Database : bdf_demo
  User     : postgres
  Password : postgres

Commandes utiles :
  # Démarrer PostgreSQL
  $ bash scripts/run_postgres.sh

  # Arrêter PostgreSQL
  $ podman stop bdf-demo-ia

  # Voir les logs
  $ podman logs bdf-demo-ia

  # Se connecter à la DB
  $ podman exec -it bdf-demo-ia psql -U postgres -d bdf_demo

📝 EXEMPLES D'UTILISATION
──────────────────────────────────────────────────────────────

1. Créer une personne :
$ curl -X POST http://localhost:8000/personnes/ \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Dupont",
    "prenom": "Jean",
    "fonction": "Développeur",
    "email_pro": "jean.dupont@bdf.fr"
  }'

2. Lister les personnes :
$ curl http://localhost:8000/personnes/

3. Créer un projet :
$ curl -X POST http://localhost:8000/projets/ \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Projet Alpha",
    "description": "Description du projet",
    "developpeur_principal_id": 1
  }'

4. Récupérer un projet avec ses relations :
$ curl http://localhost:8000/projets/1

🛠️ TECHNOLOGIES
──────────────────────────────────────────────────────────────

Backend       : FastAPI 0.123.0
ORM           : SQLAlchemy 2.0.44
Validation    : Pydantic 2.12.5
Serveur       : Uvicorn 0.38.0
Base de données : PostgreSQL 16
Driver DB     : psycopg 3.3.0
Tests         : pytest 9.0.1
Python        : 3.14

📚 DOCUMENTATION
──────────────────────────────────────────────────────────────

README.md           : Documentation complète du projet
PROJET_COMPLET.md   : Récapitulatif et état du projet
/docs               : Swagger UI (interactive)
/redoc              : ReDoc (documentation alternative)

🎯 PROCHAINES ÉTAPES
──────────────────────────────────────────────────────────────

1. Sécurité : Ajouter authentification JWT
2. Migrations : Intégrer Alembic
3. Tests : Augmenter la couverture
4. API : Ajouter filtres et pagination avancée
5. DevOps : Créer Dockerfile et CI/CD

──────────────────────────────────────────────────────────────
✅ Projet prêt pour la production !
──────────────────────────────────────────────────────────────

EOF

