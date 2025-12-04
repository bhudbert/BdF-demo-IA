#!/usr/bin/env python3
"""
Script de seed pour peupler la base de données avec des données de test
Inclut les profils, catégories, personnes et projets
"""
import sys
import os

# Ajouter le répertoire parent au chemin Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db.session import SessionLocal
from src.repositories.profile_repository import ProfileRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.person_repository import PersonRepository
from src.repositories.project_repository import ProjectRepository


def seed_profiles(db):
    """Créer les profils professionnels"""
    print("🔧 Création des profils professionnels...")

    repo = ProfileRepository(db)

    profiles_data = [
        {
            "name": "Développeur",
            "description": "Développeur logiciel"
        },
        {
            "name": "DevOps",
            "description": "Ingénieur DevOps"
        },
        {
            "name": "Chef de projet",
            "description": "Chef de projet informatique"
        },
        {
            "name": "Architecte",
            "description": "Architecte logiciel"
        },
        {
            "name": "Tech Lead",
            "description": "Lead développeur technique"
        }
    ]

    profiles = []
    for profile_data in profiles_data:
        profile = repo.create(profile_data)
        profiles.append(profile)
        print(f"  ✓ Profil créé: {profile.name}")

    return profiles


def seed_categories(db):
    """Créer les catégories de projets"""
    print("\n📁 Création des catégories de projets...")

    repo = CategoryRepository(db)

    categories_data = [
        {
            "name": "Web",
            "description": "Projets de développement web"
        },
        {
            "name": "Mobile",
            "description": "Applications mobiles"
        },
        {
            "name": "Infrastructure",
            "description": "Projets d'infrastructure et DevOps"
        },
        {
            "name": "Data",
            "description": "Projets de data science et IA"
        }
    ]

    categories = []
    for category_data in categories_data:
        category = repo.create(category_data)
        categories.append(category)
        print(f"  ✓ Catégorie créée: {category.name}")

    return categories


def seed_persons(db, profiles):
    """Créer les personnes avec profils"""
    print("\n👥 Création des personnes...")

    repo = PersonRepository(db)

    persons_data = [
        {
            "last_name": "Dupont",
            "first_name": "Marie",
            "client": "Banque de France",
            "client_city": "Paris",
            "position": "Lead Développeur",
            "professional_email": "marie.dupont@bdf.fr",
            "mobile": "06 12 34 56 78",
            "team": "Digital",
            "manager": "Jean Martin",
            "profile_id": profiles[4].id  # Tech Lead
        },
        {
            "last_name": "Martin",
            "first_name": "Pierre",
            "client": "Banque de France",
            "client_city": "Paris",
            "position": "Développeur Backend",
            "professional_email": "pierre.martin@bdf.fr",
            "mobile": "06 23 45 67 89",
            "team": "Digital",
            "manager": "Jean Martin",
            "profile_id": profiles[0].id  # Développeur
        },
        {
            "last_name": "Bernard",
            "first_name": "Sophie",
            "client": "Banque de France",
            "client_city": "Lyon",
            "position": "Chef de Projet",
            "professional_email": "sophie.bernard@bdf.fr",
            "mobile": "06 34 56 78 90",
            "team": "Projets",
            "manager": "Anne Dubois",
            "profile_id": profiles[2].id  # Chef de projet
        },
        {
            "last_name": "Leroy",
            "first_name": "Thomas",
            "client": "Banque de France",
            "client_city": "Paris",
            "position": "DevOps Engineer",
            "professional_email": "thomas.leroy@bdf.fr",
            "mobile": "06 45 67 89 01",
            "team": "Infrastructure",
            "manager": "Jean Martin",
            "profile_id": profiles[1].id  # DevOps
        },
        {
            "last_name": "Dubois",
            "first_name": "Julie",
            "client": "Banque de France",
            "client_city": "Paris",
            "position": "Architecte Logiciel",
            "professional_email": "julie.dubois@bdf.fr",
            "mobile": "06 56 78 90 12",
            "team": "Architecture",
            "manager": "Anne Dubois",
            "profile_id": profiles[3].id  # Architecte
        }
    ]

    persons = []
    for person_data in persons_data:
        person = repo.create(person_data)
        persons.append(person)
        print(f"  ✓ Personne créée: {person.first_name} {person.last_name} ({person.position})")

    return persons


def seed_projects(db, persons, categories):
    """Créer les projets avec catégories"""
    print("\n📊 Création des projets...")

    repo = ProjectRepository(db)

    projects_data = [
        {
            "name": "API Carnet d'Adresses",
            "description": "API REST pour gérer le carnet d'adresses de la BdF",
            "lead_developer_id": persons[0].id,  # Marie Dupont
            "project_manager_id": persons[2].id,  # Sophie Bernard
            "dev_line_id": persons[1].id,  # Pierre Martin
            "category_id": categories[0].id  # Web
        },
        {
            "name": "Infrastructure Cloud",
            "description": "Migration de l'infrastructure vers le cloud",
            "lead_developer_id": persons[3].id,  # Thomas Leroy
            "project_manager_id": persons[2].id,  # Sophie Bernard
            "category_id": categories[2].id  # Infrastructure
        },
        {
            "name": "Analyse de données financières",
            "description": "Système d'analyse de données avec IA",
            "lead_developer_id": persons[4].id,  # Julie Dubois
            "project_manager_id": persons[2].id,  # Sophie Bernard
            "dev_line_id": persons[0].id,  # Marie Dupont
            "category_id": categories[3].id  # Data
        }
    ]

    projects = []
    for project_data in projects_data:
        project = repo.create(project_data)
        projects.append(project)
        print(f"  ✓ Projet créé: {project.name}")

    return projects


def main():
    """Fonction principale"""
    print("🌱 Démarrage du seed de la base de données...")
    print("=" * 60)

    # Créer une session de base de données
    db = SessionLocal()

    try:
        # Créer les profils
        profiles = seed_profiles(db)

        # Créer les catégories
        categories = seed_categories(db)

        # Créer les personnes
        persons = seed_persons(db, profiles)

        # Créer les projets
        projects = seed_projects(db, persons, categories)

        print("\n" + "=" * 60)
        print("✅ Seed terminé avec succès!")
        print(f"   - {len(profiles)} profils créés")
        print(f"   - {len(categories)} catégories créées")
        print(f"   - {len(persons)} personnes créées")
        print(f"   - {len(projects)} projets créés")

    except Exception as e:
        print(f"\n❌ Erreur lors du seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

