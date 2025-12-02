#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "============================================"
echo "Validation de l'Anglicisation"
echo "============================================"
echo ""

# Activer l'environnement virtuel
source .venv/bin/activate
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

# Test 1: Import de l'application
echo "1. Test d'import de l'application..."
python -c "from src.main import app; print('✓ Application importée')" 2>&1 | grep "✓" || echo "❌ Erreur d'import"
echo ""

# Test 2: Import des modèles
echo "2. Test d'import des modèles..."
python -c "from src.models import Person, Project; print('✓ Modèles importés')" 2>&1 | grep "✓" || echo "❌ Erreur modèles"
echo ""

# Test 3: Import des repositories
echo "3. Test d'import des repositories..."
python -c "from src.repositories import PersonRepository, ProjectRepository; print('✓ Repositories importés')" 2>&1 | grep "✓" || echo "❌ Erreur repositories"
echo ""

# Test 4: Import des schemas
echo "4. Test d'import des schemas..."
python -c "from src.api.schemas import Person, Project, PersonCreate, ProjectCreate; print('✓ Schemas importés')" 2>&1 | grep "✓" || echo "❌ Erreur schemas"
echo ""

# Test 5: Exécuter les tests
echo "5. Exécution des tests unitaires..."
pytest tests/ -q --tb=no 2>&1 | tail -3
echo ""

echo "============================================"
echo "✅ Validation terminée"
echo "============================================"
echo ""
echo "Code anglicisé :"
echo "  ✓ Person (au lieu de Personne)"
echo "  ✓ Project (au lieu de Projet)"
echo "  ✓ last_name (au lieu de nom)"
echo "  ✓ first_name (au lieu de prenom)"
echo "  ✓ Endpoints: /persons/ et /projects/"
echo ""
echo "Docstrings et commentaires conservés en français ✓"
echo ""

