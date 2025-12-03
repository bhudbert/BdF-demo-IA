# Architecture Modulaire - BdF Demo IA v2.0

## 🏗️ Vue d'ensemble de l'architecture

Le projet a été réorganisé selon une architecture modulaire en couches pour faciliter la scalabilité et la maintenabilité.

```
src/
├── api/                    # Couche API (Présentation)
│   ├── routers/           # Endpoints REST
│   │   ├── personnes.py   # Routes /personnes
│   │   └── projets.py     # Routes /projets
│   └── schemas.py         # Schémas Pydantic (validation)
│
├── core/                   # Configuration centrale
│   └── config.py          # Settings de l'application
│
├── db/                     # Couche base de données
│   ├── session.py         # Configuration SQLAlchemy
│   └── base.py            # Base + imports des modèles
│
├── models/                 # Modèles de domaine
│   ├── personne.py        # Modèle Personne
│   └── projet.py          # Modèle Projet
│
├── repositories/           # Couche d'accès aux données
│   ├── base_repository.py         # Repository générique
│   ├── personne_repository.py     # Repository Personne
│   └── projet_repository.py       # Repository Projet
│
└── main.py                # Point d'entrée FastAPI
```

---

## 📦 Description des packages

### 1. **Package `api`** - Couche de présentation

**Responsabilité** : Gestion des requêtes HTTP et validation des données d'entrée/sortie

#### `api/routers/`
- Routes et endpoints REST
- Définition des verbes HTTP (GET, POST, PUT, DELETE)
- Gestion des codes de statut HTTP
- Injection de dépendances (repositories)

#### `api/schemas.py`
- Schémas Pydantic pour la validation
- Définition des DTOs (Data Transfer Objects)
- Conversion modèles ↔ JSON

**Exemples de schémas** :
- `PersonneCreate` : Données pour créer une personne
- `PersonneUpdate` : Données pour modifier une personne
- `Personne` : Réponse avec ID et données complètes

---

### 2. **Package `core`** - Configuration centrale

**Responsabilité** : Configuration globale de l'application

#### `core/config.py`
- Settings de l'application (via Pydantic)
- Configuration de la base de données
- Variables d'environnement
- URL de connexion PostgreSQL

**Avantages** :
- Configuration centralisée
- Support des variables d'environnement
- Validation des settings au démarrage

---

### 3. **Package `db`** - Gestion de la base de données

**Responsabilité** : Configuration SQLAlchemy et session DB

#### `db/session.py`
- Création du moteur SQLAlchemy
- Configuration de la session
- Classe `Base` pour les modèles
- Fonction `get_db()` pour injection de dépendances

#### `db/base.py`
- Import centralisé de tous les modèles
- Enregistrement des modèles auprès de `Base.metadata`
- Facilite la création des tables

**Pattern utilisé** : Session per Request
- Chaque requête HTTP a sa propre session DB
- Gestion automatique du commit/rollback
- Fermeture automatique de la session

---

### 4. **Package `models`** - Modèles de domaine

**Responsabilité** : Définition des entités métier et du schéma de base de données

#### `models/personne.py`
- Modèle ORM pour la table `personnes`
- Définition des colonnes et types
- Contrainte d'unicité nom/prenom
- Relations avec les projets

#### `models/projet.py`
- Modèle ORM pour la table `projets`
- Clés étrangères vers `personnes`
- Relations bidirectionnelles

**Caractéristiques** :
- Un fichier par modèle (facilite la maintenance)
- Documentation des relations
- Utilisation de SQLAlchemy 2.0 (DeclarativeBase)

---

### 5. **Package `repositories`** - Couche d'accès aux données

**Responsabilité** : Encapsulation de la logique d'accès aux données (Pattern Repository)

#### `repositories/base_repository.py`
Repository générique avec opérations CRUD de base :
- `get(id)` : Récupérer par ID
- `get_all(skip, limit)` : Lister avec pagination
- `create(obj_in)` : Créer
- `update(id, obj_in)` : Mettre à jour
- `delete(id)` : Supprimer
- `count()` : Compter

#### `repositories/personne_repository.py`
Repository spécialisé pour les personnes :
- Hérite de `BaseRepository[Personne]`
- `get_by_nom_prenom()` : Recherche par nom/prenom
- `search_by_name()` : Recherche textuelle

#### `repositories/projet_repository.py`
Repository spécialisé pour les projets :
- Hérite de `BaseRepository[Projet]`
- `get_with_relations()` : Chargement eager des relations
- `get_by_developpeur()` : Projets par développeur
- `get_by_chef_projet()` : Projets par chef de projet

**Avantages du pattern Repository** :
- Séparation entre logique métier et accès données
- Facilite les tests (mocking)
- Réutilisation du code CRUD
- Possibilité d'ajouter du caching
- Abstraction de la couche de persistance

---

## 🔄 Flux de données

### Exemple : Création d'une personne

```
1. Client HTTP → POST /personnes/
   ↓
2. api/routers/personnes.py
   - Validation via PersonneCreate (Pydantic)
   - Injection de PersonneRepository
   ↓
3. repositories/personne_repository.py
   - Appel de create() avec les données
   ↓
4. db/session.py
   - Session SQLAlchemy
   - INSERT INTO personnes
   - COMMIT
   ↓
5. Retour de l'objet créé
   ↓
6. Conversion en Personne (schema Pydantic)
   ↓
7. Réponse JSON au client
```

---

## 🎯 Principes architecturaux appliqués

### 1. **Separation of Concerns** (Séparation des préoccupations)
Chaque couche a une responsabilité unique :
- API : Gestion HTTP
- Repositories : Accès données
- Models : Représentation du domaine
- Core : Configuration

### 2. **Dependency Injection**
Utilisation de FastAPI `Depends()` pour :
- Injection de la session DB
- Injection des repositories
- Facilite les tests unitaires

### 3. **Repository Pattern**
Abstraction de l'accès aux données :
- Centralise les requêtes SQL
- Facilite les changements de DB
- Améliore la testabilité

### 4. **Single Responsibility Principle**
Un fichier/classe = une responsabilité :
- Un modèle par fichier
- Un repository par modèle
- Un router par ressource

### 5. **DRY (Don't Repeat Yourself)**
`BaseRepository` évite la duplication du code CRUD de base

---

## 🚀 Avantages de cette architecture

### Scalabilité
- ✅ Ajout facile de nouveaux modèles
- ✅ Ajout facile de nouveaux endpoints
- ✅ Ajout facile de nouvelles fonctionnalités

### Maintenabilité
- ✅ Code organisé et structuré
- ✅ Responsabilités clairement définies
- ✅ Facilité de navigation dans le code

### Testabilité
- ✅ Chaque couche testable indépendamment
- ✅ Mocking facile des repositories
- ✅ Tests isolés

### Extensibilité
- ✅ Ajout de middleware facile
- ✅ Ajout de services métier
- ✅ Intégration de caching
- ✅ Ajout d'événements/observers

---

## 📚 Ajout d'un nouveau module

### Étape 1 : Créer le modèle
```python
# src/models/nouveau_modele.py
from src.db.session import Base
from sqlalchemy import Column, Integer, String

class NouveauModele(Base):
    __tablename__ = "nouveau_modeles"
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
```

### Étape 2 : Ajouter au base.py
```python
# src/db/base.py
from src.models.nouveau_modele import NouveauModele
```

### Étape 3 : Créer les schémas
```python
# src/api/schemas.py
class NouveauModeleBase(BaseModel):
    nom: str

class NouveauModeleCreate(NouveauModeleBase):
    pass

class NouveauModele(NouveauModeleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
```

### Étape 4 : Créer le repository
```python
# src/repositories/nouveau_modele_repository.py
from src.repositories.base_repository import BaseRepository
from src.models.nouveau_modele import NouveauModele

class NouveauModeleRepository(BaseRepository[NouveauModele]):
    def __init__(self, db: Session):
        super().__init__(NouveauModele, db)
```

### Étape 5 : Créer le router
```python
# src/api/routers/nouveau_modele.py
from fastapi import APIRouter, Depends
from src.repositories.nouveau_modele_repository import NouveauModeleRepository

router = APIRouter(prefix="/nouveau-modeles", tags=["nouveau-modeles"])

def get_repository(db: Session = Depends(get_db)):
    return NouveauModeleRepository(db)

@router.get("/")
def list_items(repo: NouveauModeleRepository = Depends(get_repository)):
    return repo.get_all()
```

### Étape 6 : Enregistrer le router
```python
# src/main.py
from src.api.routers import nouveau_modele
app.include_router(nouveau_modele.router)
```

---

## 🧪 Tests

La structure modulaire facilite les tests à différents niveaux :

### Tests unitaires des repositories
```python
def test_create_personne(db_session):
    repo = PersonneRepository(db_session)
    personne = repo.create({"nom": "Test", "prenom": "User"})
    assert personne.id is not None
```

### Tests d'intégration des endpoints
```python
def test_create_personne_endpoint(client):
    response = client.post("/personnes/", json={
        "nom": "Test", "prenom": "User"
    })
    assert response.status_code == 201
```

---

## 📊 Comparaison avant/après

### Avant (structure simple)
```
src/
├── config.py
├── database.py
├── models.py          # Tous les modèles
├── schemas.py         # Tous les schémas
├── crud.py            # Toutes les fonctions CRUD
├── routers/
│   ├── personnes.py
│   └── projets.py
└── main.py
```

**Problèmes** :
- Fichiers volumineux
- Couplage fort
- Difficile à maintenir à grande échelle

### Après (structure modulaire)
```
src/
├── api/               # Couche présentation
├── core/              # Configuration
├── db/                # Base de données
├── models/            # Un fichier par modèle
├── repositories/      # Logique d'accès données
└── main.py
```

**Avantages** :
- Fichiers de taille raisonnable
- Couplage faible
- Facile à étendre
- Meilleure testabilité

---

## 🔮 Évolutions futures possibles

### Services métier
```
src/services/
├── personne_service.py
└── projet_service.py
```
Pour la logique métier complexe entre plusieurs repositories.

### Events/Messaging
```
src/events/
├── handlers/
└── publishers/
```
Pour les notifications et événements asynchrones.

### Caching
```
src/cache/
└── redis_cache.py
```
Ajout de caching au niveau des repositories.

### Background tasks
```
src/tasks/
└── celery_tasks.py
```
Pour les tâches asynchrones longues.

---

**Architecture v2.0 - Prête pour la production ! 🚀**

