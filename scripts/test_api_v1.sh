#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "============================================"
echo "Test des Nouveaux Endpoints /api/v1"
echo "============================================"
echo ""

# Activer l'environnement virtuel
source .venv/bin/activate
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

echo "1. Test d'import de l'application..."
python -c "from src.main import app; print('  ✓ Application importée')" || { echo "  ❌ Erreur"; exit 1; }
echo ""

echo "2. Test des routes enregistrées..."
python << 'EOF'
from src.main import app

print("  Routes enregistrées:")
for route in app.routes:
    if hasattr(route, 'path') and hasattr(route, 'methods'):
        methods = ', '.join(route.methods) if route.methods else 'N/A'
        print(f"    {methods:20} {route.path}")
print("")
print("  ✓ Vérifier que les routes commencent par /api/v1/persons et /api/v1/projects")
EOF
echo ""

echo "3. Exécution des tests..."
pytest tests/ -v --tb=short | tail -20
echo ""

echo "============================================"
echo "✅ Vérification terminée"
echo "============================================"
echo ""
echo "Nouveaux endpoints :"
echo "  GET/POST    /api/v1/persons/"
echo "  GET/PUT/DEL /api/v1/persons/{id}"
echo "  GET/POST    /api/v1/projects/"
echo "  GET/PUT/DEL /api/v1/projects/{id}"
echo ""
echo "Endpoints système :"
echo "  GET         /"
echo "  GET         /health"
echo "  GET         /docs"
echo ""

