#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Vérifier que l'environnement virtuel existe
if [ ! -d ".venv" ]; then
    echo "Erreur: L'environnement virtuel .venv n'existe pas."
    echo "Exécutez: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activer l'environnement virtuel
source .venv/bin/activate

# Définir PYTHONPATH
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

# Vérifier la connexion à PostgreSQL
echo "Vérification de la connexion à PostgreSQL..."
if ! podman ps | grep -q bdf-demo-ia; then
    echo "⚠️  Le conteneur PostgreSQL n'est pas démarré."
    echo "Lancement de PostgreSQL..."
    bash scripts/run_postgres.sh
    echo "Attente de l'initialisation de PostgreSQL (10 secondes)..."
    sleep 10
fi

# Créer les tables si nécessaire
echo "Création des tables dans la base de données..."
python -c "from src.database import Base, engine; Base.metadata.create_all(bind=engine); print('✓ Tables créées/vérifiées')"

# Lancer l'application
echo "Démarrage de l'application FastAPI..."
echo "API accessible sur: http://localhost:8000"
echo "Documentation: http://localhost:8000/docs"
echo ""
uvicorn src.main:app --reload --host 0.0.0.0 --port 8002

