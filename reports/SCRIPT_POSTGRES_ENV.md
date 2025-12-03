# ✅ Script run_postgres.sh Utilise Maintenant le .env !

## 🎯 Modification Effectuée

Le script `scripts/run_postgres.sh` a été modifié pour charger automatiquement les variables du fichier `.env` au lieu d'utiliser des valeurs codées en dur.

---

## 📝 Changements dans run_postgres.sh

### ❌ Avant (valeurs codées en dur)
```bash
podman run \
  --name "$CONTAINER_NAME" \
  --detach \
  --rm \
  --env POSTGRES_USER=postgres \          # ❌ Codé en dur
  --env POSTGRES_PASSWORD=postgres \      # ❌ Codé en dur
  --env POSTGRES_DB=bdf_demo \           # ❌ Codé en dur
  --publish 5434:5432 \                  # ❌ Codé en dur
  --volume "$DATA_DIR:/var/lib/postgresql/data:z" \
  "$IMAGE"
```

### ✅ Après (chargement depuis .env)
```bash
# Charger les variables depuis .env
ENV_FILE="$PROJECT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Erreur: Fichier .env introuvable"
    echo "Veuillez créer le fichier .env à partir de .env.example:"
    echo "  cp .env.example .env"
    exit 1
fi

# Charger les variables d'environnement
set -a  # Exporter automatiquement toutes les variables
source "$ENV_FILE"
set +a

# Vérifier que les variables nécessaires sont définies
if [ -z "${POSTGRES_USER:-}" ] || [ -z "${POSTGRES_PASSWORD:-}" ] || [ -z "${POSTGRES_DB:-}" ] || [ -z "${POSTGRES_PORT:-}" ]; then
    echo "❌ Erreur: Variables manquantes dans .env"
    exit 1
fi

# Utiliser les variables du .env
podman run \
  --name "$CONTAINER_NAME" \
  --detach \
  --rm \
  --env POSTGRES_USER="$POSTGRES_USER" \          # ✅ Depuis .env
  --env POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \  # ✅ Depuis .env
  --env POSTGRES_DB="$POSTGRES_DB" \             # ✅ Depuis .env
  --publish "$POSTGRES_PORT:5432" \              # ✅ Depuis .env
  --volume "$DATA_DIR:/var/lib/postgresql/data:z" \
  "$IMAGE"
```

---

## 🔄 Flux du Script

```
1. Vérifier que .env existe
   ├─ ❌ Si absent → Erreur avec message d'aide
   └─ ✅ Si présent → Continuer

2. Charger les variables depuis .env
   └─ POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT

3. Valider les variables
   ├─ ❌ Si manquantes → Erreur
   └─ ✅ Si toutes présentes → Continuer

4. Afficher la configuration
   └─ User, DB, Port (pas le password pour la sécurité)

5. Créer le répertoire de données
   └─ mkdir -p app-pgdata

6. Arrêter l'ancien conteneur si existant
   └─ podman rm -f bdf-demo-ia

7. Démarrer le nouveau conteneur
   └─ Utiliser les variables du .env
```

---

## 📊 Avantages de cette Approche

### Cohérence
✅ **Une seule source de vérité** : Le fichier `.env`
- `config.py` lit `.env` pour Python
- `run_postgres.sh` lit `.env` pour Podman
- Pas de désynchronisation possible

### Flexibilité
✅ **Changement facile** : Modifier `.env` une seule fois
```bash
# Changer le port dans .env
POSTGRES_PORT=5435

# Le script et l'application utilisent automatiquement le nouveau port
```

### Sécurité
✅ **Validation** : Le script vérifie que toutes les variables sont présentes
```bash
if [ -z "${POSTGRES_USER:-}" ] || ...; then
    echo "❌ Erreur: Variables manquantes"
    exit 1
fi
```

### Transparence
✅ **Feedback** : Le script affiche la configuration chargée
```
📝 Chargement de la configuration depuis .env...
✓ Configuration chargée:
  POSTGRES_USER: postgres
  POSTGRES_DB: bdf_demo
  POSTGRES_PORT: 5434
```

---

## 🚀 Utilisation

### Démarrage Standard
```bash
# 1. S'assurer que .env existe
cp .env.example .env

# 2. Lancer PostgreSQL (utilise automatiquement .env)
bash scripts/run_postgres.sh
```

**Sortie attendue** :
```
📝 Chargement de la configuration depuis .env...
✓ Configuration chargée:
  POSTGRES_USER: postgres
  POSTGRES_DB: bdf_demo
  POSTGRES_PORT: 5434

🗑️  Arrêt du conteneur existant si présent...
🚀 Démarrage du conteneur PostgreSQL...

✅ PostgreSQL démarré avec succès!

📊 Informations de connexion:
  Host: localhost
  Port: 5434
  Database: bdf_demo
  User: postgres
```

### Changement de Configuration

**Exemple : Changer le port**
```bash
# 1. Éditer .env
nano .env
# Changer POSTGRES_PORT=5434 en POSTGRES_PORT=5555

# 2. Relancer PostgreSQL
bash scripts/run_postgres.sh

# 3. Le conteneur démarre maintenant sur le port 5555
```

**Exemple : Changer le nom de la base**
```bash
# 1. Éditer .env
nano .env
# Changer POSTGRES_DB=bdf_demo en POSTGRES_DB=mon_projet

# 2. Relancer PostgreSQL
bash scripts/run_postgres.sh

# 3. La base s'appelle maintenant "mon_projet"
```

---

## 🛡️ Gestion des Erreurs

### Cas 1 : Fichier .env manquant
```bash
$ bash scripts/run_postgres.sh

❌ Erreur: Fichier .env introuvable
Veuillez créer le fichier .env à partir de .env.example:
  cp .env.example .env
```

### Cas 2 : Variables manquantes dans .env
```bash
$ bash scripts/run_postgres.sh

📝 Chargement de la configuration depuis .env...
❌ Erreur: Variables manquantes dans .env
Vérifiez que .env contient: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT
```

---

## 🧪 Tests

### Test 1 : Vérifier le chargement du .env
```bash
bash scripts/run_postgres.sh | head -10
```

**Résultat attendu** :
```
📝 Chargement de la configuration depuis .env...
✓ Configuration chargée:
  POSTGRES_USER: postgres
  POSTGRES_DB: bdf_demo
  POSTGRES_PORT: 5434
```

### Test 2 : Vérifier que le conteneur utilise les bonnes valeurs
```bash
# Démarrer le conteneur
bash scripts/run_postgres.sh

# Vérifier les variables d'environnement du conteneur
podman exec bdf-demo-ia env | grep POSTGRES
```

**Résultat attendu** :
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=bdf_demo
```

### Test 3 : Vérifier le port
```bash
podman ps | grep bdf-demo-ia
```

**Résultat attendu** :
```
... 0.0.0.0:5434->5432/tcp ...
```

---

## 📋 Checklist

- [x] Script modifié pour lire `.env`
- [x] Validation des variables obligatoires
- [x] Messages d'erreur clairs
- [x] Affichage de la configuration chargée
- [x] Utilisation des variables dans `podman run`
- [x] Gestion du cas où `.env` est absent
- [x] Documentation créée

---

## 🎉 Résultat

### Cohérence Totale
```
.env (source unique de vérité)
  ├─ config.py → Utilisé par Python/FastAPI
  └─ run_postgres.sh → Utilisé par Podman
```

### Plus Aucune Valeur Codée en Dur
- ❌ **Avant** : Valeurs dans `config.py` ET dans `run_postgres.sh`
- ✅ **Après** : Toutes les valeurs dans `.env`

### Configuration Centralisée
```bash
# Modifier une seule fois dans .env
POSTGRES_PORT=5555

# Tous les scripts et l'application utilisent automatiquement la nouvelle valeur
```

---

## 📝 Commandes Utiles

### Voir les logs du conteneur
```bash
podman logs bdf-demo-ia
```

### Se connecter à PostgreSQL
```bash
podman exec -it bdf-demo-ia psql -U postgres -d bdf_demo
```

### Arrêter le conteneur
```bash
podman stop bdf-demo-ia
```

### Redémarrer avec nouvelle configuration
```bash
# 1. Modifier .env
nano .env

# 2. Relancer
bash scripts/run_postgres.sh
```

---

**Script run_postgres.sh utilise maintenant .env ! ✅**

Plus aucune valeur codée en dur, tout est centralisé dans le fichier `.env` ! 🎉

