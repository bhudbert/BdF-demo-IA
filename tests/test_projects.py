from fastapi.testclient import TestClient


def test_create_project(client: TestClient):
    """Test de création d'un projet"""
    # Créer d'abord un développeur principal
    person_response = client.post(
        "/persons/",
        json={"last_name": "Dupont", "first_name": "Jean"}
    )
    dev_id = person_response.json()["id"]

    # Créer un projet
    response = client.post(
        "/projects/",
        json={
            "name": "Projet Alpha",
            "description": "Un super projet",
            "lead_developer_id": dev_id
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Projet Alpha"
    assert data["lead_developer_id"] == dev_id
    assert "id" in data


def test_create_project_without_dev_principal(client: TestClient):
    """Test de création d'un projet sans développeur principal (devrait échouer)"""
    response = client.post(
        "/projects/",
        json={
            "name": "Projet Beta",
            "description": "Un projet sans dev",
            "lead_developer_id": 999  # ID inexistant
        }
    )
    assert response.status_code == 400


def test_create_project_with_all_roles(client: TestClient):
    """Test de création d'un projet avec tous les rôles"""
    # Créer les personnes
    chef = client.post("/persons/", json={"last_name": "Chef", "first_name": "Alice"})
    ligne = client.post("/persons/", json={"last_name": "Ligne", "first_name": "Bob"})
    dev = client.post("/persons/", json={"last_name": "Dev", "first_name": "Charlie"})

    chef_id = chef.json()["id"]
    ligne_id = ligne.json()["id"]
    dev_id = dev.json()["id"]

    # Créer un projet avec tous les rôles
    response = client.post(
        "/projects/",
        json={
            "name": "Projet Complet",
            "description": "Projet avec tous les rôles",
            "project_manager_id": chef_id,
            "dev_line_id": ligne_id,
            "lead_developer_id": dev_id
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["project_manager_id"] == chef_id
    assert data["dev_line_id"] == ligne_id
    assert data["lead_developer_id"] == dev_id


def test_read_projects(client: TestClient):
    """Test de lecture de tous les projets"""
    # Créer une personne
    person = client.post("/persons/", json={"last_name": "Dev", "first_name": "Test"})
    dev_id = person.json()["id"]

    # Créer des projets
    client.post("/projects/", json={"name": "Projet 1", "lead_developer_id": dev_id})
    client.post("/projects/", json={"name": "Projet 2", "lead_developer_id": dev_id})

    # Récupérer tous les projets
    response = client.get("/projects/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_read_project(client: TestClient):
    """Test de lecture d'un projet par ID"""
    # Créer une personne
    person = client.post("/persons/", json={"last_name": "Dev", "first_name": "Test"})
    dev_id = person.json()["id"]

    # Créer un projet
    create_response = client.post(
        "/projects/",
        json={"name": "Projet Test", "lead_developer_id": dev_id}
    )
    project_id = create_response.json()["id"]

    # Récupérer le projet
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id
    assert data["name"] == "Projet Test"
    assert data["lead_developer_rel"]["last_name"] == "Dev"


def test_read_project_not_found(client: TestClient):
    """Test de lecture d'un projet inexistant"""
    response = client.get("/projects/999")
    assert response.status_code == 404


def test_update_project(client: TestClient):
    """Test de mise à jour d'un projet"""
    # Créer une personne
    person = client.post("/persons/", json={"last_name": "Dev", "first_name": "Test"})
    dev_id = person.json()["id"]

    # Créer un projet
    create_response = client.post(
        "/projects/",
        json={"name": "Projet Original", "lead_developer_id": dev_id}
    )
    project_id = create_response.json()["id"]

    # Mettre à jour le projet
    response = client.put(
        f"/projects/{project_id}",
        json={"description": "Nouvelle description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Nouvelle description"
    assert data["name"] == "Projet Original"  # Les autres champs sont préservés


def test_delete_project(client: TestClient):
    """Test de suppression d'un projet"""
    # Créer une personne
    person = client.post("/persons/", json={"last_name": "Dev", "first_name": "Test"})
    dev_id = person.json()["id"]

    # Créer un projet
    create_response = client.post(
        "/projects/",
        json={"name": "Projet à supprimer", "lead_developer_id": dev_id}
    )
    project_id = create_response.json()["id"]

    # Supprimer le projet
    response = client.delete(f"/projects/{project_id}")
    assert response.status_code == 204

    # Vérifier que le projet n'existe plus
    get_response = client.get(f"/projects/{project_id}")
    assert get_response.status_code == 404
