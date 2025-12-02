#!/usr/bin/env bash
set -euo pipefail

echo "============================================"
echo "Vidage de la base de données PostgreSQL"
echo "============================================"
echo ""

# Vérifier que le conteneur PostgreSQL est en cours d'exécution
if ! podman ps | grep -q bdf-demo-ia; then
    echo "❌ Le conteneur PostgreSQL n'est pas démarré"
    echo "Veuillez d'abord lancer : bash scripts/run_postgres.sh"
    exit 1
fi

echo "📦 Conteneur PostgreSQL trouvé"
echo ""

# Connexion à PostgreSQL et suppression des anciennes tables
echo "🗑️  Suppression des anciennes tables (personnes, projets)..."
podman exec -it bdf-demo-ia psql -U postgres -d bdf_demo -c "
    DROP TABLE IF EXISTS projets CASCADE;
    DROP TABLE IF EXISTS personnes CASCADE;
    SELECT 'Tables supprimées avec succès' AS status;
" 2>&1 | grep -E "(DROP|status|succès)" || echo "Tables déjà supprimées ou inexistantes"

echo ""
echo "🆕 Les nouvelles tables (persons, projects) seront créées au prochain démarrage de l'application"
echo ""
echo "============================================"
echo "✅ Base de données vidée"
echo "============================================"
echo ""
echo "Prochaines étapes :"
echo "  1. Nettoyer le cache Python : find . -type d -name '__pycache__' -exec rm -rf {} +"
echo "  2. Lancer l'application : bash scripts/run_app.sh"
echo ""

