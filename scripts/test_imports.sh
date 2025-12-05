#!/usr/bin/env bash
# Script de test rapide pour vérifier les imports

cd /data/devsecops/repository/build/Bruno/BdF-demo-IA
source .venv/bin/activate

echo "=== Test 1: Import des modèles ==="
python3 -c "
from src.models.task import Task
print('✓ Task model OK')
"

echo "=== Test 2: Import des schémas ==="
python3 -c "
from src.api.schemas import Task, TaskCreate, TaskUpdate
print('✓ Task schemas OK')
"

echo "=== Test 3: Import du repository ==="
python3 -c "
from src.repositories.task_repository import TaskRepository
print('✓ TaskRepository OK')
"

echo "=== Test 4: Import du router ==="
python3 -c "
from src.api.routers.tasks import router
print('✓ Tasks router OK')
"

echo "=== Test 5: Lancement de l'app ==="
python3 -c "
from src.main import app
print('✓ App OK')
print('Endpoints:', [route.path for route in app.routes if hasattr(route, 'path')])
"

echo "=== Tous les imports OK ==="

