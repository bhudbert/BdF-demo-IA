# Filtrage des Personnes et Projets

## Résumé

Ajout de deux nouveaux endpoints permettant de filtrer :
- **Les personnes par profil** : `/api/v1/persons/by-profile/{profile_id}`
- **Les projets par catégorie** : `/api/v1/projects/by-category/{category_id}`

## Nouveaux endpoints

### 1. Filtrer les personnes par profil

**Endpoint :** `GET /api/v1/persons/by-profile/{profile_id}`

**Description :** Récupère toutes les personnes ayant un profil spécifique.

**Paramètres :**
- `profile_id` (path, required) : ID du profil
- `skip` (query, optional) : Nombre d'éléments à ignorer (défaut: 0)
- `limit` (query, optional) : Nombre maximum d'éléments à retourner (défaut: 100)

**Exemples :**

```bash
# Récupérer toutes les personnes avec le profil ID 1 (Développeur)
curl http://localhost:8000/api/v1/persons/by-profile/1

# Avec pagination
curl http://localhost:8000/api/v1/persons/by-profile/1?skip=0&limit=10
```

**Réponse (200 OK) :**
```json
[
  {
    "id": 2,
    "last_name": "Martin",
    "first_name": "Pierre",
    "client": "Banque de France",
    "position": "Développeur Backend",
    "professional_email": "pierre.martin@bdf.fr",
    "profile_id": 1,
    "mobile": "06 23 45 67 89",
    "team": "Digital",
    "manager": "Jean Martin"
  }
]
```

### 2. Filtrer les projets par catégorie

**Endpoint :** `GET /api/v1/projects/by-category/{category_id}`

**Description :** Récupère tous les projets appartenant à une catégorie spécifique.

**Paramètres :**
- `category_id` (path, required) : ID de la catégorie
- `skip` (query, optional) : Nombre d'éléments à ignorer (défaut: 0)
- `limit` (query, optional) : Nombre maximum d'éléments à retourner (défaut: 100)

**Exemples :**

```bash
# Récupérer tous les projets de la catégorie ID 1 (Web)
curl http://localhost:8000/api/v1/projects/by-category/1

# Avec pagination
curl http://localhost:8000/api/v1/projects/by-category/1?skip=0&limit=10
```

**Réponse (200 OK) :**
```json
[
  {
    "id": 1,
    "name": "API Carnet d'Adresses",
    "description": "API REST pour gérer le carnet d'adresses de la BdF",
    "lead_developer_id": 1,
    "project_manager_id": 3,
    "dev_line_id": 2,
    "category_id": 1,
    "project_manager_rel": {
      "id": 3,
      "last_name": "Bernard",
      "first_name": "Sophie",
      "position": "Chef de Projet"
    },
    "dev_line_rel": {
      "id": 2,
      "last_name": "Martin",
      "first_name": "Pierre"
    },
    "lead_developer_rel": {
      "id": 1,
      "last_name": "Dupont",
      "first_name": "Marie"
    }
  }
]
```

## Modifications techniques

### Repositories

#### PersonRepository (`src/repositories/person_repository.py`)

Nouvelle méthode ajoutée :
```python
def get_by_profile(self, profile_id: int, skip: int = 0, limit: int = 100) -> List[Person]:
    """Récupérer toutes les personnes d'un profil donné"""
    return self.db.query(self.model).filter(
        self.model.profile_id == profile_id
    ).offset(skip).limit(limit).all()
```

#### ProjectRepository (`src/repositories/project_repository.py`)

Nouvelle méthode ajoutée :
```python
def get_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
    """Récupérer tous les projets d'une catégorie donnée"""
    return self.db.query(self.model).filter(
        self.model.category_id == category_id
    ).offset(skip).limit(limit).all()
```

### Routers

#### PersonsRouter (`src/api/routers/persons.py`)

Nouveau endpoint ajouté :
```python
@router.get("/by-profile/{profile_id}", response_model=List[schemas.Person])
def read_persons_by_profile(
    profile_id: int,
    skip: int = 0,
    limit: int = 100,
    repository: PersonRepository = Depends(get_repository)
):
    """Récupérer toutes les personnes d'un profil donné"""
    persons = repository.get_by_profile(profile_id, skip=skip, limit=limit)
    return persons
```

#### ProjectsRouter (`src/api/routers/projects.py`)

Nouveau endpoint ajouté :
```python
@router.get("/by-category/{category_id}", response_model=List[schemas.Project])
def read_projects_by_category(
    category_id: int,
    skip: int = 0,
    limit: int = 100,
    repository: ProjectRepository = Depends(get_project_repository)
):
    """Récupérer tous les projets d'une catégorie donnée"""
    projects = repository.get_by_category(category_id, skip=skip, limit=limit)
    return projects
```

## Tests

Un nouveau fichier de tests a été créé : `tests/test_filtering.py`

**Tests inclus :**
- ✅ `test_get_persons_by_profile` - Filtrage basique des personnes
- ✅ `test_get_persons_by_profile_empty` - Profil sans personnes
- ✅ `test_get_projects_by_category` - Filtrage basique des projets
- ✅ `test_get_projects_by_category_empty` - Catégorie sans projets
- ✅ `test_get_persons_by_profile_with_pagination` - Pagination des personnes
- ✅ `test_get_projects_by_category_with_pagination` - Pagination des projets

**Exécuter les tests :**
```bash
python -m pytest tests/test_filtering.py -v
```

## Cas d'usage

### Exemple 1 : Lister tous les développeurs

```bash
# 1. Récupérer l'ID du profil "Développeur"
curl http://localhost:8000/api/v1/profiles | jq '.[] | select(.name=="Développeur")'

# 2. Utiliser l'ID pour filtrer les personnes
curl http://localhost:8000/api/v1/persons/by-profile/1
```

### Exemple 2 : Lister tous les projets Web

```bash
# 1. Récupérer l'ID de la catégorie "Web"
curl http://localhost:8000/api/v1/categories | jq '.[] | select(.name=="Web")'

# 2. Utiliser l'ID pour filtrer les projets
curl http://localhost:8000/api/v1/projects/by-category/1
```

### Exemple 3 : Statistiques par profil

```python
from src.db.session import SessionLocal
from src.repositories.profile_repository import ProfileRepository
from src.repositories.person_repository import PersonRepository

db = SessionLocal()
profile_repo = ProfileRepository(db)
person_repo = PersonRepository(db)

# Afficher le nombre de personnes par profil
for profile in profile_repo.get_all():
    count = len(person_repo.get_by_profile(profile.id))
    print(f"{profile.name}: {count} personne(s)")
```

### Exemple 4 : Statistiques par catégorie

```python
from src.db.session import SessionLocal
from src.repositories.category_repository import CategoryRepository
from src.repositories.project_repository import ProjectRepository

db = SessionLocal()
category_repo = CategoryRepository(db)
project_repo = ProjectRepository(db)

# Afficher le nombre de projets par catégorie
for category in category_repo.get_all():
    count = len(project_repo.get_by_category(category.id))
    print(f"{category.name}: {count} projet(s)")
```

## Scripts de test

Un script de démonstration a été créé : `scripts/test_filtering.py`

**Exécution :**
```bash
python scripts/test_filtering.py
```

**Sortie attendue :**
```
🧪 TEST DES NOUVEAUX ENDPOINTS DE FILTRAGE
============================================================
TEST: PERSONNES PAR PROFIL
============================================================

📋 Profil: Développeur
  • Pierre Martin - Développeur Backend

📋 Profil: DevOps
  • Thomas Leroy - DevOps Engineer

📋 Profil: Chef de projet
  • Sophie Bernard - Chef de Projet

📋 Profil: Architecte
  • Julie Dubois - Architecte Logiciel

📋 Profil: Tech Lead
  • Marie Dupont - Lead Développeur

============================================================
TEST: PROJETS PAR CATÉGORIE
============================================================

📁 Catégorie: Web
  • API Carnet d'Adresses - Lead: Marie Dupont

📁 Catégorie: Mobile
  (Aucun projet dans cette catégorie)

📁 Catégorie: Infrastructure
  • Infrastructure Cloud - Lead: Thomas Leroy

📁 Catégorie: Data
  • Analyse de données financières - Lead: Julie Dubois

============================================================
✅ TOUS LES TESTS SONT PASSÉS!
============================================================
```

## Documentation Swagger

Les nouveaux endpoints sont automatiquement documentés dans Swagger UI :

**Accès :** http://localhost:8000/docs

Vous y trouverez :
- La description complète des endpoints
- Les paramètres acceptés
- Les modèles de réponse
- Un outil interactif pour tester les endpoints

## Résumé des changements

### Fichiers modifiés
- ✅ `src/repositories/person_repository.py` - Ajout de `get_by_profile()`
- ✅ `src/repositories/project_repository.py` - Ajout de `get_by_category()`
- ✅ `src/api/routers/persons.py` - Ajout de l'endpoint `/by-profile/{profile_id}`
- ✅ `src/api/routers/projects.py` - Ajout de l'endpoint `/by-category/{category_id}`

### Fichiers créés
- ✅ `tests/test_filtering.py` - Tests unitaires complets
- ✅ `scripts/test_filtering.py` - Script de démonstration
- ✅ `reports/FILTRAGE_DOCUMENTATION.md` - Cette documentation

### Tests
- ✅ **6 tests unitaires** passent avec succès
- ✅ **Script de démonstration** fonctionne correctement
- ✅ **Pagination** testée et validée

## Conclusion

Les fonctionnalités de filtrage sont maintenant **opérationnelles** et **testées** :
- 🎯 Filtrage des personnes par profil
- 🎯 Filtrage des projets par catégorie
- 🎯 Support de la pagination
- 🎯 Tests unitaires complets
- 🎯 Documentation complète

Ces endpoints facilitent grandement la recherche et l'organisation des données dans l'API ! 🚀

