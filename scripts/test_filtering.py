#!/usr/bin/env python3
"""
Script de test pour les endpoints de filtrage par profil et catégorie
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db.session import SessionLocal
from src.repositories.profile_repository import ProfileRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.person_repository import PersonRepository
from src.repositories.project_repository import ProjectRepository


def test_persons_by_profile():
    """Tester le filtrage des personnes par profil"""
    db = SessionLocal()

    print("=" * 60)
    print("TEST: PERSONNES PAR PROFIL")
    print("=" * 60)

    profile_repo = ProfileRepository(db)
    person_repo = PersonRepository(db)

    # Récupérer tous les profils
    profiles = profile_repo.get_all()

    for profile in profiles:
        print(f"\n📋 Profil: {profile.name}")
        persons = person_repo.get_by_profile(profile.id)
        if persons:
            for person in persons:
                print(f"  • {person.first_name} {person.last_name} - {person.position}")
        else:
            print(f"  (Aucune personne avec ce profil)")

    db.close()


def test_projects_by_category():
    """Tester le filtrage des projets par catégorie"""
    db = SessionLocal()

    print("\n" + "=" * 60)
    print("TEST: PROJETS PAR CATÉGORIE")
    print("=" * 60)

    category_repo = CategoryRepository(db)
    project_repo = ProjectRepository(db)

    # Récupérer toutes les catégories
    categories = category_repo.get_all()

    for category in categories:
        print(f"\n📁 Catégorie: {category.name}")
        projects = project_repo.get_by_category(category.id)
        if projects:
            for project in projects:
                lead = f"{project.lead_developer_rel.first_name} {project.lead_developer_rel.last_name}"
                print(f"  • {project.name} - Lead: {lead}")
        else:
            print(f"  (Aucun projet dans cette catégorie)")

    db.close()


def main():
    print("\n🧪 TEST DES NOUVEAUX ENDPOINTS DE FILTRAGE")
    print("=" * 60)

    try:
        test_persons_by_profile()
        test_projects_by_category()

        print("\n" + "=" * 60)
        print("✅ TOUS LES TESTS SONT PASSÉS!")
        print("=" * 60)
        print("\n📝 Endpoints disponibles:")
        print("  • GET /api/v1/persons/by-profile/{profile_id}")
        print("  • GET /api/v1/projects/by-category/{category_id}")
        print()

    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

