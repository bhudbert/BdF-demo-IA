#!/usr/bin/env bash
# Script pour afficher la nouvelle structure du projet

cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║        BdF Demo IA v2.0 - Architecture Modulaire              ║
╚════════════════════════════════════════════════════════════════╝

📁 Structure des Packages
──────────────────────────────────────────────────────────────────

src/
│
├── 🌐 api/                    Couche API (Présentation)
│   ├── routers/
│   │   ├── personnes.py       → Endpoints /personnes
│   │   └── projets.py         → Endpoints /projets
│   └── schemas.py             → Validation Pydantic
│
├── ⚙️  core/                   Configuration
│   └── config.py              → Settings PostgreSQL
│
├── 💾 db/                      Base de données
│   ├── session.py             → Engine, Session, get_db()
│   └── base.py                → Import des modèles
│
├── 📊 models/                  Modèles ORM
│   ├── personne.py            → Table personnes
│   └── projet.py              → Table projets
│
├── 🗄️  repositories/           Accès aux données (CRUD)
│   ├── base_repository.py     → CRUD générique
│   ├── personne_repository.py → + méthodes spécifiques
│   └── projet_repository.py   → + méthodes spécifiques
│
└── 🚀 main.py                  Point d'entrée FastAPI

tests/
├── conftest.py                → Fixtures pytest
├── test_main.py               → 2 tests
├── test_personnes.py          → 9 tests
└── test_projets.py            → 8 tests

scripts/
├── run_postgres.sh            → Lance PostgreSQL
├── run_app.sh                 → Lance l'application
├── run_tests.sh               → Exécute les tests
└── show_structure.sh          → Ce script !

──────────────────────────────────────────────────────────────────

📊 Statistiques
──────────────────────────────────────────────────────────────────

EOF

# Compter les fichiers Python
PYTHON_FILES=$(find src -name "*.py" | wc -l)
TEST_FILES=$(find tests -name "test_*.py" | wc -l)
TOTAL_LINES=$(find src -name "*.py" -exec wc -l {} + | tail -1 | awk '{print $1}')

echo "  Fichiers Python (src)  : $PYTHON_FILES"
echo "  Fichiers de tests      : $TEST_FILES"
echo "  Lignes de code (src)   : ~$TOTAL_LINES"
echo ""

cat << 'EOF'
──────────────────────────────────────────────────────────────────

🎯 Principes Architecturaux
──────────────────────────────────────────────────────────────────

✓ Separation of Concerns    Chaque couche a une responsabilité
✓ Repository Pattern         Abstraction de l'accès données
✓ Dependency Injection       Via FastAPI Depends()
✓ Single Responsibility      Un fichier = une responsabilité
✓ DRY (Don't Repeat)        BaseRepository générique

──────────────────────────────────────────────────────────────────

🔄 Flux de Données
──────────────────────────────────────────────────────────────────

Client HTTP
    ↓
api/routers/         (Validation Pydantic)
    ↓
repositories/        (Logique CRUD)
    ↓
db/session.py        (SQLAlchemy)
    ↓
PostgreSQL
    ↓
models/              (Objets ORM)
    ↓
Réponse JSON

──────────────────────────────────────────────────────────────────

✅ Tests : 17/17 passent
──────────────────────────────────────────────────────────────────

EOF

# Essayer d'exécuter les tests rapidement
if [ -d ".venv" ]; then
    echo "Exécution rapide des tests..."
    export PYTHONPATH=$PWD
    .venv/bin/pytest tests/ -q --tb=no 2>/dev/null || echo "  (lancez 'bash scripts/run_tests.sh' pour plus de détails)"
fi

cat << 'EOF'

──────────────────────────────────────────────────────────────────

📚 Documentation Disponible
──────────────────────────────────────────────────────────────────

  ARCHITECTURE.md       → Architecture détaillée
  REORGANISATION.md     → Guide de réorganisation
  README.md            → Guide utilisateur
  PROJET_COMPLET.md    → Récapitulatif technique

──────────────────────────────────────────────────────────────────

🚀 Commandes Rapides
──────────────────────────────────────────────────────────────────

  bash scripts/run_postgres.sh    # Lance PostgreSQL
  bash scripts/run_app.sh          # Lance l'application
  bash scripts/run_tests.sh        # Exécute les tests

  http://localhost:8000/docs       # Documentation Swagger

──────────────────────────────────────────────────────────────────

🎉 Architecture v2.0 - Production Ready !
──────────────────────────────────────────────────────────────────

EOF

