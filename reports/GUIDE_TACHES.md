# Guide d'Utilisation - Gestion des Tâches

## 🚀 Démarrage rapide

### 1. Réinitialiser la base de données
```bash
./scripts/reset_database.sh
```

### 2. Lancer l'application
```bash
./scripts/run_app.sh
```

### 3. Accéder à la documentation
Ouvrez votre navigateur : http://localhost:8000/docs

## 📋 Exemples d'utilisation

### Créer un profil
```bash
curl -X POST "http://localhost:8000/api/v1/profiles/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Développeur Backend", "description": "Expert API REST"}'
```

### Créer une personne
```bash
curl -X POST "http://localhost:8000/api/v1/persons/" \
  -H "Content-Type: application/json" \
  -d '{
    "last_name": "Dupont",
    "first_name": "Jean",
    "client": "Banque de France",
    "position": "Développeur Senior",
    "professional_email": "jean.dupont@bdf.fr",
    "mobile": "0601020304",
    "profile_id": 1
  }'
```

### Créer une catégorie
```bash
curl -X POST "http://localhost:8000/api/v1/categories/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Application Web", "description": "Applications web modernes"}'
```

### Créer un projet
```bash
curl -X POST "http://localhost:8000/api/v1/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API de Gestion",
    "description": "API REST pour la gestion des ressources",
    "lead_developer_id": 1,
    "category_id": 1
  }'
```

### 🎯 Créer une tâche
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Développer endpoint authentification",
    "description": "Implémenter JWT et OAuth2",
    "start_date": "2025-12-05",
    "end_date": "2025-12-15",
    "project_id": 1,
    "assigned_person_id": 1
  }'
```

### Lister toutes les tâches
```bash
curl "http://localhost:8000/api/v1/tasks/"
```

### Obtenir une tâche spécifique
```bash
curl "http://localhost:8000/api/v1/tasks/1"
```

### Lister les tâches d'un projet
```bash
curl "http://localhost:8000/api/v1/tasks/by-project/1"
```

### Lister les tâches d'une personne
```bash
curl "http://localhost:8000/api/v1/tasks/by-person/1"
```

### Obtenir les tâches actives aujourd'hui
```bash
curl "http://localhost:8000/api/v1/tasks/active/"
```

### Obtenir les tâches actives à une date précise
```bash
curl "http://localhost:8000/api/v1/tasks/active/?current_date=2025-12-10"
```

### Mettre à jour une tâche
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Développer endpoint authentification (v2)",
    "description": "Implémenter JWT, OAuth2 et 2FA",
    "end_date": "2025-12-20"
  }'
```

### Supprimer une tâche
```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/1"
```

## 🧪 Lancer les tests

### Tous les tests
```bash
./scripts/run_tests.sh
```

### Tests des tâches uniquement
```bash
./scripts/run_tests.sh tests/test_tasks.py -v
```

### Un test spécifique
```bash
./scripts/run_tests.sh tests/test_tasks.py::test_create_task -v
```

## 📊 Structure des données

### Tâche (Task)
```json
{
  "id": 1,
  "title": "Développer API",
  "description": "Description détaillée",
  "start_date": "2025-12-05",
  "end_date": "2025-12-15",
  "project_id": 1,
  "assigned_person_id": 1
}
```

## ⚠️ Règles de validation

1. **Dates** : La date de fin doit être >= à la date de début
2. **Projet** : Le projet doit exister avant de créer une tâche
3. **Personne** : La personne doit exister avant de créer une tâche
4. **Titre** : Ne peut pas être vide
5. **Dates** : Sont obligatoires (start_date et end_date)

## 🔍 Codes de statut HTTP

- `200 OK` : Succès (GET, PUT)
- `201 Created` : Création réussie (POST)
- `204 No Content` : Suppression réussie (DELETE)
- `400 Bad Request` : Données invalides (dates, etc.)
- `404 Not Found` : Ressource non trouvée

## 💡 Astuces

### Pagination
Tous les endpoints de liste supportent la pagination :
```bash
curl "http://localhost:8000/api/v1/tasks/?skip=0&limit=10"
```

### Documentation interactive
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

### Santé de l'API
```bash
curl "http://localhost:8000/health"
```

## 🐛 Dépannage

### La base de données n'est pas à jour
```bash
./scripts/reset_database.sh
```

### Les tests échouent
```bash
# Nettoyer le cache
find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null
rm -rf .pytest_cache

# Relancer les tests
./scripts/run_tests.sh
```

### Vérifier les imports
```bash
./scripts/test_imports.sh
```

## 📚 Documentation complète

Consultez le fichier `reports/AJOUT_GESTION_TACHES.md` pour plus de détails sur l'implémentation.

