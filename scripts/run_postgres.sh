#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$PROJECT_DIR/app-pgdata"
CONTAINER_NAME="bdf-demo-ia"
IMAGE="docker.io/library/postgres:16"

# Charger les variables depuis le fichier .env
ENV_FILE="$PROJECT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Erreur: Fichier .env introuvable"
    echo "Veuillez créer le fichier .env à partir de .env.example:"
    echo "  cp .env.example .env"
    exit 1
fi

echo "📝 Chargement de la configuration depuis .env..."

# Charger les variables d'environnement depuis .env
set -a  # Exporter automatiquement toutes les variables
source "$ENV_FILE"
set +a

# Vérifier que les variables nécessaires sont définies
if [ -z "${POSTGRES_USER:-}" ] || [ -z "${POSTGRES_PASSWORD:-}" ] || [ -z "${POSTGRES_DB:-}" ] || [ -z "${POSTGRES_PORT:-}" ]; then
    echo "❌ Erreur: Variables manquantes dans .env"
    echo "Vérifiez que .env contient: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT"
    exit 1
fi

echo "✓ Configuration chargée:"
echo "  POSTGRES_USER: $POSTGRES_USER"
echo "  POSTGRES_DB: $POSTGRES_DB"
echo "  POSTGRES_PORT: $POSTGRES_PORT"
echo ""

mkdir -p "$DATA_DIR"

echo "🗑️  Arrêt du conteneur existant si présent..."
podman rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

echo "🚀 Démarrage du conteneur PostgreSQL..."
podman run \
  --name "$CONTAINER_NAME" \
  --detach \
  --rm \
  --env POSTGRES_USER="$POSTGRES_USER" \
  --env POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  --env POSTGRES_DB="$POSTGRES_DB" \
  --publish "$POSTGRES_PORT:5432" \
  --volume "$DATA_DIR:/var/lib/postgresql/data:z" \
  "$IMAGE"

echo ""
echo "✅ PostgreSQL démarré avec succès!"
echo ""
echo "📊 Informations de connexion:"
echo "  Host: localhost"
echo "  Port: $POSTGRES_PORT"
echo "  Database: $POSTGRES_DB"
echo "  User: $POSTGRES_USER"
echo ""
echo "🔍 Commandes utiles:"
echo "  podman logs $CONTAINER_NAME        # Voir les logs"
echo "  podman stop $CONTAINER_NAME        # Arrêter"
echo "  podman exec -it $CONTAINER_NAME psql -U $POSTGRES_USER -d $POSTGRES_DB  # Se connecter"
echo ""

