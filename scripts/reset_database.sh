#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$PROJECT_DIR/.env"

echo "============================================"
echo "Vidage de la base de données PostgreSQL"
echo "============================================"
echo ""

# Charger les variables depuis .env
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Le fichier .env n'existe pas"
    echo "Veuillez créer le fichier .env : cp .env.example .env"
    exit 1
fi

set -a
source "$ENV_FILE"
set +a

# Vérifier que le conteneur PostgreSQL est en cours d'exécution
if ! podman ps | grep -q bdf-demo-ia; then
    echo "❌ Le conteneur PostgreSQL n'est pas démarré"
    echo "Veuillez d'abord lancer : bash scripts/run_postgres.sh"
    exit 1
fi

echo "📦 Conteneur PostgreSQL trouvé"
echo "📝 Configuration depuis .env : $POSTGRES_DB"
echo ""

# Connexion à PostgreSQL et suppression des anciennes tables
echo "🗑️  Suppression de toutes les tables..."
podman exec -it bdf-demo-ia psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "
    DROP TABLE IF EXISTS projets CASCADE;
    DROP TABLE IF EXISTS personnes CASCADE;
    DROP TABLE IF EXISTS projects CASCADE;
    DROP TABLE IF EXISTS persons CASCADE;
    DROP TABLE IF EXISTS categories CASCADE;
    DROP TABLE IF EXISTS profiles CASCADE;
    SELECT 'Tables supprimées avec succès' AS status;
" 2>&1 | grep -E "(DROP|status|succès)" || echo "Tables déjà supprimées ou inexistantes"

echo ""
echo "🆕 Les nouvelles tables (persons, projects, categories, profiles) seront créées au prochain démarrage de l'application"
echo ""
echo "============================================"
echo "✅ Base de données vidée"
echo "============================================"
echo ""
echo "Prochaines étapes :"
echo "  1. Nettoyer le cache Python : find . -type d -name '__pycache__' -exec rm -rf {} +"
echo "  2. Lancer l'application : bash scripts/run_app.sh"
echo ""

