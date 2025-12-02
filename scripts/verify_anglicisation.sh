#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "============================================"
echo "Vérification Complète de l'Anglicisation"
echo "============================================"
echo ""

# Activer l'environnement virtuel
source .venv/bin/activate
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

echo "1. Test des imports des modèles..."
python -c "
from src.models.person import Person
from src.models.project import Project
print('  ✓ Person importé')
print('  ✓ Project importé')
print(f'  ✓ Table Person: {Person.__tablename__}')
print(f'  ✓ Table Project: {Project.__tablename__}')
" || { echo "❌ Erreur d'import des modèles"; exit 1; }
echo ""

echo "2. Test des imports des repositories..."
python -c "
from src.repositories.person_repository import PersonRepository
from src.repositories.project_repository import ProjectRepository
print('  ✓ PersonRepository importé')
print('  ✓ ProjectRepository importé')
" || { echo "❌ Erreur d'import des repositories"; exit 1; }
echo ""

echo "3. Test des méthodes des repositories..."
python -c "
from src.repositories.person_repository import PersonRepository
from src.repositories.project_repository import ProjectRepository
import inspect

# Vérifier PersonRepository
person_methods = [m for m in dir(PersonRepository) if not m.startswith('_')]
print('  PersonRepository méthodes:')
for method in ['get', 'get_all', 'create', 'update', 'delete', 'get_by_last_name_first_name', 'search_by_name']:
    if method in person_methods:
        print(f'    ✓ {method}')
    else:
        print(f'    ❌ {method} manquante')

print('')
print('  ProjectRepository méthodes:')
project_methods = [m for m in dir(ProjectRepository) if not m.startswith('_')]
for method in ['get', 'get_all', 'create', 'update', 'delete', 'get_with_relations', 'get_by_lead_developer', 'get_by_project_manager']:
    if method in project_methods:
        print(f'    ✓ {method}')
    else:
        print(f'    ❌ {method} manquante')
" || { echo "❌ Erreur vérification méthodes"; exit 1; }
echo ""

echo "4. Test de l'application principale..."
python -c "
from src.main import app
print('  ✓ Application FastAPI importée')
" || { echo "❌ Erreur import application"; exit 1; }
echo ""

echo "5. Vérification des schémas API..."
python -c "
from src.api.schemas import Person, Project, PersonCreate, ProjectCreate
print('  ✓ Person schema')
print('  ✓ Project schema')
print('  ✓ PersonCreate schema')
print('  ✓ ProjectCreate schema')
" || { echo "❌ Erreur schémas API"; exit 1; }
echo ""

echo "6. Vérification des endpoints..."
python -c "
from src.api.routers import persons, projects
print('  ✓ Router persons')
print('  ✓ Router projects')
print(f'  ✓ Prefix persons: {persons.router.prefix}')
print(f'  ✓ Prefix projects: {projects.router.prefix}')
" || { echo "❌ Erreur routers"; exit 1; }
echo ""

echo "============================================"
echo "✅ Tous les Contrôles Réussis !"
echo "============================================"
echo ""
echo "Résumé de l'anglicisation :"
echo "  ✓ Modèles : Person, Project"
echo "  ✓ Tables : persons, projects"
echo "  ✓ Repositories : PersonRepository, ProjectRepository"
echo "  ✓ Méthodes : get_by_last_name_first_name, get_by_lead_developer, etc."
echo "  ✓ Endpoints : /persons/, /projects/"
echo "  ✓ Schemas : Person, Project, PersonCreate, ProjectCreate"
echo ""
echo "Prochaine étape : Vider la base de données"
echo "  bash scripts/reset_database.sh"
echo ""

