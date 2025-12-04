#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "📂 Répertoire du projet : $PROJECT_DIR"cd .
cd "$PROJECT_DIR"

# Activer l'environnement virtuel
if [ ! -d ".venv" ]; then
    echo "Erreur: L'environnement virtuel .venv n'existe pas."
    exit 1
fi

source .venv/bin/activate

# Définir PYTHONPATH
export PYTHONPATH="$PROJECT_DIR"

# Exécuter les tests
echo "Exécution des tests..."
pytest tests/ -v --tb=short --cov=src --cov-report=term-missing "$@"

