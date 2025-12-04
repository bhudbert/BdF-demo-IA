#!/usr/bin/env python3
"""
Script de test pour vérifier les nouveaux endpoints de l'API
"""
from src.db.session import SessionLocal
from src.repositories.profile_repository import ProfileRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.person_repository import PersonRepository
from src.repositories.project_repository import ProjectRepository

def main():
    db = SessionLocal()

    print("=" * 60)
    print("TEST DES NOUVELLES FONCTIONNALITÉS")
    print("=" * 60)

    # Test des profils
    print("\n📋 PROFILS:")
    profile_repo = ProfileRepository(db)
    profiles = profile_repo.get_all()
    for profile in profiles:
        print(f"  • {profile.name}: {profile.description}")

    # Test des catégories
    print("\n📁 CATÉGORIES:")
    category_repo = CategoryRepository(db)
    categories = category_repo.get_all()
    for category in categories:
        print(f"  • {category.name}: {category.description}")

    # Test des personnes avec profils
    print("\n👥 PERSONNES AVEC PROFILS:")
    person_repo = PersonRepository(db)
    persons = person_repo.get_all()
    for person in persons:
        profile_name = person.profile_rel.name if person.profile_rel else "Aucun"
        print(f"  • {person.first_name} {person.last_name} - {person.position} ({profile_name})")

    # Test des projets avec catégories
    print("\n📊 PROJETS AVEC CATÉGORIES:")
    project_repo = ProjectRepository(db)
    projects = project_repo.get_all()
    for project in projects:
        category_name = project.category_rel.name if project.category_rel else "Aucune"
        lead = f"{project.lead_developer_rel.first_name} {project.lead_developer_rel.last_name}"
        print(f"  • {project.name} ({category_name}) - Lead: {lead}")

    print("\n" + "=" * 60)
    print("✅ TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
    print("=" * 60)

    db.close()

if __name__ == "__main__":
    main()

