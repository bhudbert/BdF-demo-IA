# 📝 Configuration avec Variables d'Environnement

## 🎯 Fichiers de Configuration

Le projet utilise maintenant des variables d'environnement pour la configuration, ce qui permet :
- ✅ Sécurité : Les mots de passe ne sont plus dans le code
- ✅ Flexibilité : Configuration différente par environnement (dev, test, prod)
- ✅ Best Practice : Suit le principe des 12-factor apps

---

## 📁 Fichiers Créés

### 1. `.env` (à la racine)
**Fichier de configuration local** - Contient les valeurs réelles.

```dotenv
# Configuration PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=bdf_demo
POSTGRES_HOST=localhost
POSTGRES_PORT=5434
```

⚠️ **Important** : Ce fichier est dans `.gitignore` et **ne doit JAMAIS être commité**.

### 2. `.env.example` (à la racine)
**Template de configuration** - À commiter dans Git.

```dotenv
# Configuration PostgreSQL
# Ces valeurs correspondent au script run_postgres.sh
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=bdf_demo
POSTGRES_HOST=localhost
POSTGRES_PORT=5434
```

✅ Ce fichier sert de documentation et de template pour les nouveaux développeurs.

### 3. `.gitignore` (mis à jour)
```gitignore
# Variables d'environnement
.env
```

---

## 🔧 Configuration dans config.py

### Avant (valeurs codées en dur)
```python
class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"          # ❌ Codé en dur
    POSTGRES_PASSWORD: str = "postgres"      # ❌ Codé en dur
    POSTGRES_DB: str = "bdf_demo"           # ❌ Codé en dur
    POSTGRES_HOST: str = "localhost"        # ❌ Codé en dur
    POSTGRES_PORT: int = 5434               # ❌ Codé en dur
```

### Après (lecture depuis .env)
```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",                    # ✅ Lit depuis .env
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    POSTGRES_USER: str                      # ✅ Pas de valeur par défaut
    POSTGRES_PASSWORD: str                  # ✅ Pas de valeur par défaut
    POSTGRES_DB: str                        # ✅ Pas de valeur par défaut
    POSTGRES_HOST: str                      # ✅ Pas de valeur par défaut
    POSTGRES_PORT: int                      # ✅ Pas de valeur par défaut
```

---

## 🚀 Utilisation

### 1. Installation Initiale

Si vous clonez le projet :
```bash
# Copier le template
cp .env.example .env

# Éditer avec vos valeurs locales
nano .env
```

### 2. Configuration PostgreSQL

Les valeurs dans `.env` correspondent au script `scripts/run_postgres.sh` :
```bash
podman run -d \
  --name bdf-demo-ia \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=bdf_demo \
  -p 5434:5432 \
  docker.io/library/postgres:16-alpine
```

### 3. Modification pour un Autre Environnement

**Développement Local** (`.env`) :
```dotenv
POSTGRES_HOST=localhost
POSTGRES_PORT=5434
```

**Production** (variables d'environnement système) :
```bash
export POSTGRES_HOST=db.production.com
export POSTGRES_PORT=5432
export POSTGRES_PASSWORD=SecurePasswordHere
```

---

## 🔍 Vérification

### Test de Chargement
```bash
python -c "from src.core.config import settings; print(settings.database_url)"
```

**Résultat attendu** :
```
postgresql+psycopg://postgres:postgres@localhost:5434/bdf_demo
```

### Test de l'Application
```bash
python -c "from src.main import app; print('✓ Application OK')"
```

---

## 🌍 Environnements Différents

### Développement
```dotenv
# .env (local)
POSTGRES_HOST=localhost
POSTGRES_PORT=5434
POSTGRES_DB=bdf_demo
```

### Test
```dotenv
# .env.test
POSTGRES_HOST=localhost
POSTGRES_PORT=5435
POSTGRES_DB=bdf_demo_test
```

### Production
```bash
# Variables d'environnement système (pas de fichier .env)
export POSTGRES_HOST=production-db.example.com
export POSTGRES_PORT=5432
export POSTGRES_USER=app_user
export POSTGRES_PASSWORD=SecureP@ssw0rd
export POSTGRES_DB=bdf_demo_prod
```

---

## 📊 Priorité des Variables

Pydantic Settings charge les variables dans cet ordre (du moins prioritaire au plus prioritaire) :

1. **Valeurs par défaut** dans le code (supprimées dans notre cas)
2. **Fichier `.env`** à la racine
3. **Variables d'environnement système**

Exemple :
```bash
# .env contient POSTGRES_PORT=5434
# Mais on peut le surcharger :
export POSTGRES_PORT=5555
python app.py  # Utilisera 5555
```

---

## 🔐 Sécurité

### ✅ À Faire
- ✅ Ajouter `.env` au `.gitignore`
- ✅ Commiter `.env.example` dans Git
- ✅ Documenter les variables nécessaires
- ✅ Utiliser des mots de passe forts en production
- ✅ Restreindre les permissions du fichier `.env`

### ❌ À Ne Pas Faire
- ❌ Commiter le fichier `.env` dans Git
- ❌ Partager `.env` par email/chat
- ❌ Utiliser les mêmes credentials dev/prod
- ❌ Mettre des secrets dans le code

### Protection du Fichier .env
```bash
# Restreindre les permissions (Linux/Mac)
chmod 600 .env

# Vérifier
ls -la .env
# Résultat attendu : -rw------- (lecture/écriture owner uniquement)
```

---

## 🆕 Ajout de Nouvelles Variables

### 1. Ajouter dans `.env`
```dotenv
NEW_SETTING=value
```

### 2. Ajouter dans `.env.example`
```dotenv
# Description de la variable
NEW_SETTING=default_value
```

### 3. Ajouter dans `config.py`
```python
class Settings(BaseSettings):
    # ...existing code...
    NEW_SETTING: str
```

### 4. Utiliser dans le code
```python
from src.core.config import settings

print(settings.NEW_SETTING)
```

---

## 🧪 Tests

Les tests utilisent SQLite en mémoire, donc ils **ne dépendent pas** de PostgreSQL ni du fichier `.env`.

Si vous voulez tester avec PostgreSQL :
```python
# tests/conftest.py
@pytest.fixture
def test_settings():
    return Settings(
        POSTGRES_HOST="localhost",
        POSTGRES_PORT=5434,
        POSTGRES_DB="bdf_demo_test"
    )
```

---

## 📋 Checklist Migration

- [x] Créer `.env` à la racine
- [x] Créer `.env.example` à la racine
- [x] Ajouter `.env` au `.gitignore`
- [x] Modifier `config.py` pour lire depuis `.env`
- [x] Supprimer les valeurs par défaut du code
- [x] Tester le chargement de la configuration
- [x] Documenter les variables

---

## 🎉 Avantages de cette Approche

### Sécurité
- Les credentials ne sont plus dans le code
- Fichier `.env` ignoré par Git
- Mots de passe différents par environnement

### Flexibilité
- Configuration différente dev/test/prod
- Pas besoin de modifier le code
- Override facile avec variables système

### Best Practices
- Suit le principe des 12-factor apps
- Standard de l'industrie
- Facilite le déploiement

### Maintenabilité
- Configuration centralisée
- Documentation claire (`.env.example`)
- Facile à comprendre pour nouveaux devs

---

**Configuration avec .env implémentée ! ✅**

