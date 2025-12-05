#!/usr/bin/env bash
# Script pour peupler la base avec des données de test incluant des tâches

set -e

BASE_URL="http://localhost:8000/api/v1"

echo "🌱 Peuplement de la base de données avec des tâches..."
echo ""

# Créer des profils
echo "📋 Création des profils..."
PROFILE1=$(curl -s -X POST "$BASE_URL/profiles/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Développeur Backend", "description": "Expert en API REST et bases de données"}')
PROFILE1_ID=$(echo $PROFILE1 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Profil Développeur Backend créé (ID: $PROFILE1_ID)"

PROFILE2=$(curl -s -X POST "$BASE_URL/profiles/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Chef de Projet", "description": "Gestion de projets informatiques"}')
PROFILE2_ID=$(echo $PROFILE2 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Profil Chef de Projet créé (ID: $PROFILE2_ID)"

echo ""

# Créer des personnes
echo "👥 Création des personnes..."
PERSON1=$(curl -s -X POST "$BASE_URL/persons/" \
  -H "Content-Type: application/json" \
  -d '{
    "last_name": "Dupont",
    "first_name": "Jean",
    "client": "Banque de France",
    "client_city": "Paris",
    "position": "Développeur Senior",
    "professional_email": "jean.dupont@bdf.fr",
    "mobile": "0601020304",
    "team": "Team Backend",
    "profile_id": '$PROFILE1_ID'
  }')
PERSON1_ID=$(echo $PERSON1 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Jean Dupont créé (ID: $PERSON1_ID)"

PERSON2=$(curl -s -X POST "$BASE_URL/persons/" \
  -H "Content-Type: application/json" \
  -d '{
    "last_name": "Martin",
    "first_name": "Sophie",
    "client": "Banque de France",
    "client_city": "Paris",
    "position": "Chef de Projet",
    "professional_email": "sophie.martin@bdf.fr",
    "mobile": "0602030405",
    "team": "Team Management",
    "profile_id": '$PROFILE2_ID'
  }')
PERSON2_ID=$(echo $PERSON2 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Sophie Martin créée (ID: $PERSON2_ID)"

PERSON3=$(curl -s -X POST "$BASE_URL/persons/" \
  -H "Content-Type: application/json" \
  -d '{
    "last_name": "Leroy",
    "first_name": "Pierre",
    "client": "Banque de France",
    "client_city": "Lyon",
    "position": "Développeur Junior",
    "professional_email": "pierre.leroy@bdf.fr",
    "mobile": "0603040506",
    "team": "Team Backend",
    "profile_id": '$PROFILE1_ID'
  }')
PERSON3_ID=$(echo $PERSON3 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Pierre Leroy créé (ID: $PERSON3_ID)"

echo ""

# Créer des catégories
echo "🏷️  Création des catégories..."
CATEGORY1=$(curl -s -X POST "$BASE_URL/categories/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Application Web", "description": "Applications web modernes"}')
CATEGORY1_ID=$(echo $CATEGORY1 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Catégorie Application Web créée (ID: $CATEGORY1_ID)"

CATEGORY2=$(curl -s -X POST "$BASE_URL/categories/" \
  -H "Content-Type: application/json" \
  -d '{"name": "API REST", "description": "Services REST et microservices"}')
CATEGORY2_ID=$(echo $CATEGORY2 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Catégorie API REST créée (ID: $CATEGORY2_ID)"

echo ""

# Créer des projets
echo "📦 Création des projets..."
PROJECT1=$(curl -s -X POST "$BASE_URL/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API de Gestion des Ressources",
    "description": "API REST pour la gestion centralisée des ressources",
    "project_manager_id": '$PERSON2_ID',
    "lead_developer_id": '$PERSON1_ID',
    "category_id": '$CATEGORY2_ID'
  }')
PROJECT1_ID=$(echo $PROJECT1 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Projet API de Gestion créé (ID: $PROJECT1_ID)"

PROJECT2=$(curl -s -X POST "$BASE_URL/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Portail Web Interne",
    "description": "Application web pour la gestion interne",
    "project_manager_id": '$PERSON2_ID',
    "lead_developer_id": '$PERSON1_ID',
    "category_id": '$CATEGORY1_ID'
  }')
PROJECT2_ID=$(echo $PROJECT2 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Projet Portail Web créé (ID: $PROJECT2_ID)"

echo ""

# Créer des tâches
echo "✅ Création des tâches..."
TODAY=$(date +%Y-%m-%d)
NEXT_WEEK=$(date -d "+7 days" +%Y-%m-%d)
TWO_WEEKS=$(date -d "+14 days" +%Y-%m-%d)
YESTERDAY=$(date -d "-1 day" +%Y-%m-%d)

TASK1=$(curl -s -X POST "$BASE_URL/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Développer endpoint authentification",
    "description": "Implémenter JWT et OAuth2 pour l'\''authentification sécurisée",
    "start_date": "'$TODAY'",
    "end_date": "'$NEXT_WEEK'",
    "project_id": '$PROJECT1_ID',
    "assigned_person_id": '$PERSON1_ID'
  }')
TASK1_ID=$(echo $TASK1 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Tâche: Développer endpoint authentification créée (ID: $TASK1_ID)"

TASK2=$(curl -s -X POST "$BASE_URL/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Créer les tests unitaires",
    "description": "Tests complets pour tous les endpoints avec pytest",
    "start_date": "'$TODAY'",
    "end_date": "'$TWO_WEEKS'",
    "project_id": '$PROJECT1_ID',
    "assigned_person_id": '$PERSON3_ID'
  }')
TASK2_ID=$(echo $TASK2 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Tâche: Créer les tests unitaires créée (ID: $TASK2_ID)"

TASK3=$(curl -s -X POST "$BASE_URL/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Concevoir l'\''interface utilisateur",
    "description": "Design de l'\''interface web responsive avec React",
    "start_date": "'$TODAY'",
    "end_date": "'$NEXT_WEEK'",
    "project_id": '$PROJECT2_ID',
    "assigned_person_id": '$PERSON1_ID'
  }')
TASK3_ID=$(echo $TASK3 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Tâche: Concevoir l'interface utilisateur créée (ID: $TASK3_ID)"

TASK4=$(curl -s -X POST "$BASE_URL/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Documentation API",
    "description": "Rédiger la documentation complète de l'\''API",
    "start_date": "'$NEXT_WEEK'",
    "end_date": "'$TWO_WEEKS'",
    "project_id": '$PROJECT1_ID',
    "assigned_person_id": '$PERSON3_ID'
  }')
TASK4_ID=$(echo $TASK4 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Tâche: Documentation API créée (ID: $TASK4_ID)"

TASK5=$(curl -s -X POST "$BASE_URL/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tâche terminée",
    "description": "Cette tâche est terminée (date passée)",
    "start_date": "'$YESTERDAY'",
    "end_date": "'$YESTERDAY'",
    "project_id": '$PROJECT2_ID',
    "assigned_person_id": '$PERSON1_ID'
  }')
TASK5_ID=$(echo $TASK5 | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
echo "✓ Tâche: Tâche terminée créée (ID: $TASK5_ID)"

echo ""
echo "✨ Base de données peuplée avec succès !"
echo ""
echo "📊 Résumé :"
echo "  - 2 profils"
echo "  - 3 personnes"
echo "  - 2 catégories"
echo "  - 2 projets"
echo "  - 5 tâches"
echo ""
echo "🔍 Pour voir les données :"
echo "  - Personnes:      curl $BASE_URL/persons/"
echo "  - Projets:        curl $BASE_URL/projects/"
echo "  - Tâches:         curl $BASE_URL/tasks/"
echo "  - Tâches actives: curl $BASE_URL/tasks/active/"
echo ""
echo "📖 Documentation: http://localhost:8000/docs"

