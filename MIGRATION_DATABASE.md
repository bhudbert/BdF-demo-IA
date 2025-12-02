# 🔄 Procédure de Migration - Anciennes → Nouvelles Tables

## 📋 Contexte

Les modèles ont été anglicisés :
- `Personne` → `Person` (table `personnes` → `persons`)
- `Projet` → `Project` (table `projets` → `projects`)

La base de données doit être vidée pour recréer les tables avec les nouveaux noms.

---

## 🚀 Procédure de Migration

### Étape 1 : Arrêter l'application si elle tourne

```bash
# Si l'application est en cours d'exécution, l'arrêter
# Ctrl+C dans le terminal où elle tourne
```

### Étape 2 : Vérifier que PostgreSQL est démarré

```bash
podman ps | grep bdf-demo-ia
```

Si PostgreSQL n'est pas démarré :
```bash
bash scripts/run_postgres.sh
sleep 5  # Attendre l'initialisation
```

### Étape 3 : Vider la base de données

```bash
bash scripts/reset_database.sh
```

**OU manuellement** :
```bash
podman exec -it bdf-demo-ia psql -U postgres -d bdf_demo -c "
    DROP TABLE IF EXISTS projets CASCADE;
    DROP TABLE IF EXISTS personnes CASCADE;
"
```

### Étape 4 : Nettoyer le cache Python

```bash
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
rm -rf .pytest_cache
```

### Étape 5 : Vérifier les modèles

```bash
cd /data/devsecops/repository/build/Bruno/BdF-demo-IA
export PYTHONPATH=$PWD
.venv/bin/python -c "
from src.models import Person, Project
print(f'✓ Person.__tablename__ = {Person.__tablename__}')
print(f'✓ Project.__tablename__ = {Project.__tablename__}')
"
```

**Résultat attendu** :
```
✓ Person.__tablename__ = persons
✓ Project.__tablename__ = projects
```

### Étape 6 : Relancer l'application

```bash
bash scripts/run_app.sh
```

**OU manuellement** :
```bash
source .venv/bin/activate
export PYTHONPATH=$PWD
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Les nouvelles tables `persons` et `projects` seront automatiquement créées au démarrage.

### Étape 7 : Vérifier les nouvelles tables

```bash
podman exec -it bdf-demo-ia psql -U postgres -d bdf_demo -c "\dt"
```

**Résultat attendu** :
```
         List of relations
 Schema |   Name   | Type  |  Owner
--------+----------+-------+----------
 public | persons  | table | postgres
 public | projects | table | postgres
```

### Étape 8 : Tester les nouveaux endpoints

```bash
# Créer une personne
curl -X POST http://localhost:8000/persons/ \
  -H "Content-Type: application/json" \
  -d '{
    "last_name": "Dupont",
    "first_name": "Jean",
    "position": "Développeur"
  }'

# Lister les personnes
curl http://localhost:8000/persons/

# Créer un projet
curl -X POST http://localhost:8000/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Projet Alpha",
    "lead_developer_id": 1
  }'

# Lister les projets
curl http://localhost:8000/projects/
```

---

## 🧪 Exécuter les Tests

```bash
export PYTHONPATH=$PWD
.venv/bin/pytest tests/ -v
```

---

## 📊 Changements dans la Base de Données

### Anciennes Tables (supprimées)

| Table | Colonnes principales |
|-------|---------------------|
| `personnes` | id, nom, prenom, fonction, email_pro... |
| `projets` | id, nom, chef_projet_id, developpeur_principal_id... |

### Nouvelles Tables (créées)

| Table | Colonnes principales |
|-------|---------------------|
| `persons` | id, last_name, first_name, position, professional_email... |
| `projects` | id, name, project_manager_id, lead_developer_id... |

---

## 🔍 Vérifications Finales

### 1. Vérifier les modèles Python
```bash
python -c "from src.models import Person, Project; print('OK')"
```

### 2. Vérifier l'application
```bash
python -c "from src.main import app; print('OK')"
```

### 3. Vérifier les tables en base
```bash
podman exec -it bdf-demo-ia psql -U postgres -d bdf_demo -c "
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
"
```

### 4. Vérifier les colonnes
```bash
# Colonnes de persons
podman exec -it bdf-demo-ia psql -U postgres -d bdf_demo -c "
\d persons
"

# Colonnes de projects
podman exec -it bdf-demo-ia psql -U postgres -d bdf_demo -c "
\d projects
"
```

---

## ⚠️ Troubleshooting

### Problème : "Table personnes does not exist"
**Solution** : Les anciennes tables sont encore référencées. Nettoyer le cache Python.
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### Problème : "Cannot import name Person"
**Solution** : Le fichier models/person.py contient encore l'ancienne classe `Personne`.
Vérifier :
```bash
grep "class Person" src/models/person.py
```

### Problème : Tests échouent
**Solution** : Les tests utilisent SQLite en mémoire, ils ne sont pas affectés par PostgreSQL.
Si les tests échouent, c'est probablement un problème dans le code Python.

---

## 📝 Résumé de la Migration

✅ **Anciens noms** : `Personne`, `Projet`, `personnes`, `projets`  
✅ **Nouveaux noms** : `Person`, `Project`, `persons`, `projects`  
✅ **Endpoints** : `/persons/`, `/projects/` (au lieu de `/personnes/`, `/projets/`)  
✅ **Champs** : `last_name`, `first_name`, `position`, `lead_developer_id`, etc.  

---

## 🎉 Migration Complète !

Une fois la procédure terminée, votre application utilisera les nouveaux noms anglicisés avec les nouvelles tables en base de données.

---

_Script de migration automatique : `scripts/reset_database.sh`_

