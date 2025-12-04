# Script de Seed v2 - Guide d'utilisation

## Description

Le script `seed_api_v2.py` permet de peupler la base de données avec des données de test incluant les nouvelles entités **Profiles** et **Categories**.

## Contenu du seed

### 1. Profils professionnels (5)
- **Développeur** - Développeur logiciel
- **DevOps** - Ingénieur DevOps
- **Chef de projet** - Chef de projet informatique
- **Architecte** - Architecte logiciel
- **Tech Lead** - Lead développeur technique

### 2. Catégories de projets (4)
- **Web** - Projets de développement web
- **Mobile** - Applications mobiles
- **Infrastructure** - Projets d'infrastructure et DevOps
- **Data** - Projets de data science et IA

### 3. Personnes (5)
Toutes les personnes travaillent pour la Banque de France et ont un profil assigné :

1. **Marie Dupont** - Lead Développeur (Tech Lead)
2. **Pierre Martin** - Développeur Backend (Développeur)
3. **Sophie Bernard** - Chef de Projet (Chef de projet)
4. **Thomas Leroy** - DevOps Engineer (DevOps)
5. **Julie Dubois** - Architecte Logiciel (Architecte)

### 4. Projets (3)
Chaque projet a une catégorie et est lié à des personnes :

1. **API Carnet d'Adresses** (Web)
   - Lead: Marie Dupont
   - Chef de projet: Sophie Bernard
   - Dev Line: Pierre Martin

2. **Infrastructure Cloud** (Infrastructure)
   - Lead: Thomas Leroy
   - Chef de projet: Sophie Bernard

3. **Analyse de données financières** (Data)
   - Lead: Julie Dubois
   - Chef de projet: Sophie Bernard
   - Dev Line: Marie Dupont

## Utilisation

### Prérequis
- Base de données PostgreSQL en cours d'exécution
- Tables créées (ou le script créera les tables automatiquement)

### Commande
```bash
python scripts/seed_api_v2.py
```

### Réinitialisation complète
Si vous voulez repartir de zéro :

```bash
# 1. Réinitialiser la base de données
./scripts/reset_database.sh

# 2. Créer les tables
python -c "from src.db.session import engine, Base; from src.models import Person, Project, Category, Profile; Base.metadata.create_all(bind=engine)"

# 3. Insérer les données
python scripts/seed_api_v2.py
```

## Sortie attendue

```
🌱 Démarrage du seed de la base de données...
============================================================
🔧 Création des profils professionnels...
  ✓ Profil créé: Développeur
  ✓ Profil créé: DevOps
  ✓ Profil créé: Chef de projet
  ✓ Profil créé: Architecte
  ✓ Profil créé: Tech Lead

📁 Création des catégories de projets...
  ✓ Catégorie créée: Web
  ✓ Catégorie créée: Mobile
  ✓ Catégorie créée: Infrastructure
  ✓ Catégorie créée: Data

👥 Création des personnes...
  ✓ Personne créée: Marie Dupont (Lead Développeur)
  ✓ Personne créée: Pierre Martin (Développeur Backend)
  ✓ Personne créée: Sophie Bernard (Chef de Projet)
  ✓ Personne créée: Thomas Leroy (DevOps Engineer)
  ✓ Personne créée: Julie Dubois (Architecte Logiciel)

📊 Création des projets...
  ✓ Projet créé: API Carnet d'Adresses
  ✓ Projet créé: Infrastructure Cloud
  ✓ Projet créé: Analyse de données financières

============================================================
✅ Seed terminé avec succès!
   - 5 profils créés
   - 4 catégories créées
   - 5 personnes créées
   - 3 projets créés
```

## Vérification

Après le seed, vous pouvez vérifier les données via l'API :

```bash
# Lancer l'API
bash scripts/run_app.sh

# Dans un autre terminal, tester les endpoints
curl http://localhost:8000/api/v1/profiles
curl http://localhost:8000/api/v1/categories
curl http://localhost:8000/api/v1/persons
curl http://localhost:8000/api/v1/projects
```

Ou via le script de test :
```bash
python scripts/test_new_features.py
```

## Gestion des erreurs

### Erreur de doublon (UniqueViolation)
Si vous obtenez une erreur de contrainte unique, les données existent déjà. Options :
- Supprimer les données : `./scripts/reset_database.sh`
- Modifier le script pour gérer les doublons

### Erreur de colonne manquante
Si vous obtenez `column "profile_id" does not exist`, recréez les tables :
```bash
./scripts/reset_database.sh
python -c "from src.db.session import engine, Base; from src.models import Person, Project, Category, Profile; Base.metadata.create_all(bind=engine)"
```

## Personnalisation

Pour ajouter vos propres données, modifiez les sections dans `seed_api_v2.py` :
- `seed_profiles()` - Ajouter des profils
- `seed_categories()` - Ajouter des catégories
- `seed_persons()` - Ajouter des personnes
- `seed_projects()` - Ajouter des projets

