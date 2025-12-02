#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "============================================"
echo "Validation du projet BdF Demo IA"
echo "============================================"
echo ""

# 1. Vérifier l'environnement virtuel
echo "1. Vérification de l'environnement virtuel..."
if [ ! -d ".venv" ]; then
    echo "❌ Environnement virtuel manquant"
    exit 1
fi
echo "✓ Environnement virtuel présent"
echo ""

# 2. Vérifier les fichiers requis
echo "2. Vérification des fichiers du projet..."
REQUIRED_FILES=(
    "src/config.py"
    "src/database.py"
    "src/models.py"
    "src/schemas.py"
    "src/crud.py"
    "src/main.py"
    "src/routers/personnes.py"
    "src/routers/projets.py"
    "tests/conftest.py"
    "tests/test_main.py"
    "tests/test_personnes.py"
    "tests/test_projets.py"
    "requirements.txt"
    "requirements-dev.txt"
    "README.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "❌ $file manquant"
        exit 1
    fi
done
echo ""

# 3. Vérifier les dépendances
echo "3. Vérification des dépendances..."
source .venv/bin/activate
python -c "import fastapi, sqlalchemy, pydantic, pytest, httpx, uvicorn, psycopg" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Toutes les dépendances sont installées"
else
    echo "❌ Certaines dépendances manquent"
    exit 1
fi
echo ""

# 4. Tester l'import de l'application
echo "4. Vérification de l'import de l'application..."
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"
python -c "from src.main import app; print('✓ Application importée avec succès')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Impossible d'importer l'application"
    exit 1
fi
echo ""

# 5. Exécuter les tests
echo "5. Exécution des tests..."
pytest tests/ -v --tb=short -q 2>&1 | tail -5
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "✓ Tous les tests passent"
else
    echo "⚠️  Certains tests échouent (voir ci-dessus)"
fi
echo ""

# 6. Résumé
echo "============================================"
echo "✅ Validation du projet terminée"
echo "============================================"
echo ""
echo "Structure du projet :"
echo "  - Code source : src/"
echo "  - Tests : tests/ (17 tests)"
echo "  - Scripts : scripts/"
echo ""
echo "Commandes disponibles :"
echo "  bash scripts/run_postgres.sh  # Lancer PostgreSQL"
echo "  bash scripts/run_app.sh       # Lancer l'application"
echo "  bash scripts/run_tests.sh     # Exécuter les tests"
echo ""
echo "Documentation :"
echo "  - README.md : Documentation complète"
echo "  - PROJET_COMPLET.md : Récapitulatif du projet"
echo ""

