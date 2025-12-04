# Ajout des entités Category et Profile

## Résumé des modifications

J'ai ajouté avec succès la gestion des **catégories pour les projets** et des **profils pour les personnes** dans votre API.

### Nouvelles entités créées

#### 1. **Profile** (Profils professionnels)
- Représente le type de fonction d'une personne
- Champs : `id`, `name`, `description`
- Exemples : Développeur, DevOps, Chef de projet, Architecte, Tech Lead

#### 2. **Category** (Catégories de projets)
- Représente la catégorie d'un projet
- Champs : `id`, `name`, `description`
- Exemples : Web, Mobile, Infrastructure, Data

### Modifications apportées

#### Modèles (`src/models/`)
- ✅ Création de `category.py` - Modèle Category
- ✅ Création de `profile.py` - Modèle Profile
- ✅ Mise à jour de `person.py` - Ajout du champ `profile_id` et relation `profile_rel`
- ✅ Mise à jour de `project.py` - Ajout du champ `category_id` et relation `category_rel`
- ✅ Mise à jour de `__init__.py` - Export des nouveaux modèles

#### Schémas (`src/api/schemas.py`)
- ✅ Ajout des schémas `CategoryBase`, `CategoryCreate`, `CategoryUpdate`, `Category`
- ✅ Ajout des schémas `ProfileBase`, `ProfileCreate`, `ProfileUpdate`, `Profile`
- ✅ Mise à jour de `PersonBase`, `PersonUpdate` - Ajout du champ `profile_id`
- ✅ Mise à jour de `ProjectBase`, `ProjectUpdate` - Ajout du champ `category_id`

#### Repositories (`src/repositories/`)
- ✅ Création de `category_repository.py` - Repository pour Category
- ✅ Création de `profile_repository.py` - Repository pour Profile
- ✅ Mise à jour de `__init__.py` - Export des nouveaux repositories

#### Routers (`src/api/routers/`)
- ✅ Création de `categories.py` - Endpoints CRUD pour les catégories
- ✅ Création de `profiles.py` - Endpoints CRUD pour les profils

#### Application principale (`src/main.py`)
- ✅ Ajout des routers categories et profiles
- ✅ Mise à jour de la documentation de l'endpoint racine

#### Scripts
- ✅ Création de `seed_api_v2.py` - Script de seed avec les nouvelles entités
- ✅ Mise à jour de `reset_database.sh` - Suppression des nouvelles tables
- ✅ Création de `test_new_features.py` - Script de test des nouvelles fonctionnalités

### Nouveaux endpoints disponibles

#### Profiles
- `POST /api/v1/profiles` - Créer un profil
- `GET /api/v1/profiles` - Liste des profils
- `GET /api/v1/profiles/{id}` - Détails d'un profil
- `PUT /api/v1/profiles/{id}` - Mettre à jour un profil
- `DELETE /api/v1/profiles/{id}` - Supprimer un profil

#### Categories
- `POST /api/v1/categories` - Créer une catégorie
- `GET /api/v1/categories` - Liste des catégories
- `GET /api/v1/categories/{id}` - Détails d'une catégorie
- `PUT /api/v1/categories/{id}` - Mettre à jour une catégorie
- `DELETE /api/v1/categories/{id}` - Supprimer une catégorie

### Données de test insérées

Le script `seed_api_v2.py` a inséré :
- **5 profils** : Développeur, DevOps, Chef de projet, Architecte, Tech Lead
- **4 catégories** : Web, Mobile, Infrastructure, Data
- **5 personnes** avec leurs profils respectifs
- **3 projets** avec leurs catégories respectives

### Pour utiliser

1. **Réinitialiser la base de données :**
   ```bash
   ./scripts/reset_database.sh
   ```

2. **Créer les tables :**
   ```bash
   python -c "from src.db.session import engine, Base; from src.models import Person, Project, Category, Profile; Base.metadata.create_all(bind=engine); print('Tables créées')"
   ```

3. **Insérer les données de test :**
   ```bash
   python scripts/seed_api_v2.py
   ```

4. **Lancer l'API :**
   ```bash
   bash scripts/run_app.sh
   ```

5. **Tester les nouveaux endpoints :**
   ```bash
   curl http://localhost:8000/api/v1/profiles
   curl http://localhost:8000/api/v1/categories
   ```

### Structure de la base de données

```
profiles
├── id (PK)
├── name (UNIQUE)
└── description

categories
├── id (PK)
├── name (UNIQUE)
└── description

persons
├── id (PK)
├── ... (autres champs)
└── profile_id (FK → profiles.id)

projects
├── id (PK)
├── ... (autres champs)
└── category_id (FK → categories.id)
```

### Résultat du seed

```
✅ Seed terminé avec succès!
   - 5 profils créés
   - 4 catégories créées
   - 5 personnes créées
   - 3 projets créés
```

Toutes les fonctionnalités demandées ont été implémentées avec succès ! 🎉

