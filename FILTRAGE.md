# Nouveaux Endpoints de Filtrage 🔍

## Vue d'ensemble

L'API dispose maintenant de deux nouveaux endpoints permettant de filtrer les données :

### 📋 Personnes par Profil
```http
GET /api/v1/persons/by-profile/{profile_id}
```
Récupère toutes les personnes ayant un profil spécifique (Développeur, DevOps, Chef de projet, etc.)

### 📁 Projets par Catégorie
```http
GET /api/v1/projects/by-category/{category_id}
```
Récupère tous les projets appartenant à une catégorie spécifique (Web, Mobile, Infrastructure, Data)

## Exemples d'utilisation

### Lister tous les développeurs
```bash
curl http://localhost:8000/api/v1/persons/by-profile/1
```

### Lister tous les projets Web
```bash
curl http://localhost:8000/api/v1/projects/by-category/1
```

### Avec pagination
```bash
curl "http://localhost:8000/api/v1/persons/by-profile/1?skip=0&limit=10"
```

## Test rapide

```bash
# Démonstration des fonctionnalités
python scripts/test_filtering.py

# Tests unitaires
python -m pytest tests/test_filtering.py -v
```

## Documentation complète

Voir : `reports/FILTRAGE_DOCUMENTATION.md`

---

*✅ 6 tests unitaires | 📚 Documentation complète | 🚀 Prêt à l'emploi*

