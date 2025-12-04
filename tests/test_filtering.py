"""
Tests pour les endpoints de filtrage par profil et catégorie
"""
from fastapi.testclient import TestClient


def test_get_persons_by_profile(client: TestClient):
    """Test de récupération des personnes par profil"""
    # Créer un profil
    profile_response = client.post(
        "/api/v1/profiles/",
        json={"name": "Développeur Test", "description": "Profil de test"}
    )
    assert profile_response.status_code == 201
    profile_id = profile_response.json()["id"]

    # Créer des personnes avec ce profil
    client.post(
        "/api/v1/persons/",
        json={
            "last_name": "Test1",
            "first_name": "User1",
            "profile_id": profile_id
        }
    )
    client.post(
        "/api/v1/persons/",
        json={
            "last_name": "Test2",
            "first_name": "User2",
            "profile_id": profile_id
        }
    )

    # Créer une personne avec un autre profil (ou sans profil)
    client.post(
        "/api/v1/persons/",
        json={
            "last_name": "Other",
            "first_name": "User"
        }
    )

    # Récupérer les personnes avec le profil de test
    response = client.get(f"/api/v1/persons/by-profile/{profile_id}")
    assert response.status_code == 200
    data = response.json()

    # Vérifier qu'on a bien 2 personnes
    assert len(data) == 2

    # Vérifier que toutes les personnes ont le bon profile_id
    for person in data:
        assert person["profile_id"] == profile_id


def test_get_persons_by_profile_empty(client: TestClient):
    """Test de récupération des personnes par profil vide"""
    # Créer un profil sans personnes
    profile_response = client.post(
        "/api/v1/profiles/",
        json={"name": "Profil Vide", "description": "Aucune personne"}
    )
    profile_id = profile_response.json()["id"]

    # Récupérer les personnes avec ce profil
    response = client.get(f"/api/v1/persons/by-profile/{profile_id}")
    assert response.status_code == 200
    data = response.json()

    # Vérifier qu'on a une liste vide
    assert len(data) == 0


def test_get_projects_by_category(client: TestClient):
    """Test de récupération des projets par catégorie"""
    # Créer une catégorie
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Test Category", "description": "Catégorie de test"}
    )
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # Créer une personne pour être le lead developer
    person_response = client.post(
        "/api/v1/persons/",
        json={
            "last_name": "Developer",
            "first_name": "Lead"
        }
    )
    person_id = person_response.json()["id"]

    # Créer des projets avec cette catégorie
    client.post(
        "/api/v1/projects/",
        json={
            "name": "Projet Test 1",
            "description": "Description test 1",
            "lead_developer_id": person_id,
            "category_id": category_id
        }
    )
    client.post(
        "/api/v1/projects/",
        json={
            "name": "Projet Test 2",
            "description": "Description test 2",
            "lead_developer_id": person_id,
            "category_id": category_id
        }
    )

    # Créer un projet avec une autre catégorie (ou sans catégorie)
    client.post(
        "/api/v1/projects/",
        json={
            "name": "Autre Projet",
            "description": "Description autre",
            "lead_developer_id": person_id
        }
    )

    # Récupérer les projets avec la catégorie de test
    response = client.get(f"/api/v1/projects/by-category/{category_id}")
    assert response.status_code == 200
    data = response.json()

    # Vérifier qu'on a bien 2 projets
    assert len(data) == 2

    # Vérifier que tous les projets ont la bonne category_id
    for project in data:
        assert project["category_id"] == category_id


def test_get_projects_by_category_empty(client: TestClient):
    """Test de récupération des projets par catégorie vide"""
    # Créer une catégorie sans projets
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Catégorie Vide", "description": "Aucun projet"}
    )
    category_id = category_response.json()["id"]

    # Récupérer les projets avec cette catégorie
    response = client.get(f"/api/v1/projects/by-category/{category_id}")
    assert response.status_code == 200
    data = response.json()

    # Vérifier qu'on a une liste vide
    assert len(data) == 0


def test_get_persons_by_profile_with_pagination(client: TestClient):
    """Test de pagination pour les personnes par profil"""
    # Créer un profil
    profile_response = client.post(
        "/api/v1/profiles/",
        json={"name": "Profil Pagination", "description": "Test pagination"}
    )
    profile_id = profile_response.json()["id"]

    # Créer 5 personnes avec ce profil
    for i in range(5):
        client.post(
            "/api/v1/persons/",
            json={
                "last_name": f"Test{i}",
                "first_name": f"User{i}",
                "profile_id": profile_id
            }
        )

    # Récupérer les 3 premières personnes
    response = client.get(f"/api/v1/persons/by-profile/{profile_id}?skip=0&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    # Récupérer les 2 suivantes
    response = client.get(f"/api/v1/persons/by-profile/{profile_id}?skip=3&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_projects_by_category_with_pagination(client: TestClient):
    """Test de pagination pour les projets par catégorie"""
    # Créer une catégorie
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Catégorie Pagination", "description": "Test pagination"}
    )
    category_id = category_response.json()["id"]

    # Créer une personne pour être le lead developer
    person_response = client.post(
        "/api/v1/persons/",
        json={
            "last_name": "Dev",
            "first_name": "Pagination"
        }
    )
    person_id = person_response.json()["id"]

    # Créer 5 projets avec cette catégorie
    for i in range(5):
        client.post(
            "/api/v1/projects/",
            json={
                "name": f"Projet Pagination {i}",
                "description": f"Description {i}",
                "lead_developer_id": person_id,
                "category_id": category_id
            }
        )

    # Récupérer les 3 premiers projets
    response = client.get(f"/api/v1/projects/by-category/{category_id}?skip=0&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    # Récupérer les 2 suivants
    response = client.get(f"/api/v1/projects/by-category/{category_id}?skip=3&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

