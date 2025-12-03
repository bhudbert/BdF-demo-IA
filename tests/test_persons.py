from fastapi.testclient import TestClient


def test_create_person(client: TestClient):
    """Test de création d'une personne"""
    response = client.post(
        "/api/v1/persons/",
        json={
            "last_name": "Dupont",
            "first_name": "Jean",
            "client": "BdF",
            "position": "Développeur",
            "professional_email": "jean.dupont@bdf.fr"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["last_name"] == "Dupont"
    assert data["first_name"] == "Jean"
    assert "id" in data


def test_create_person_duplicate(client: TestClient):
    """Test de création d'une personne en doublon (nom/prenom unique)"""
    person_data = {
        "last_name": "Martin",
        "first_name": "Sophie"
    }
    # Première création
    response1 = client.post("/api/v1/persons/", json=person_data)
    assert response1.status_code == 201

    # Deuxième création (devrait échouer)
    response2 = client.post("/api/v1/persons/", json=person_data)
    assert response2.status_code == 400


def test_read_persons(client: TestClient):
    """Test de lecture de toutes les personnes"""
    # Créer quelques personnes
    client.post("/api/v1/persons/", json={"last_name": "Dupont", "first_name": "Jean"})
    client.post("/api/v1/persons/", json={"last_name": "Martin", "first_name": "Sophie"})

    # Récupérer toutes les personnes
    response = client.get("/api/v1/persons/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_read_person(client: TestClient):
    """Test de lecture d'une personne par ID"""
    # Créer une personne
    create_response = client.post(
        "/api/v1/persons/",
        json={"last_name": "Lefebvre", "first_name": "Marie"}
    )
    person_id = create_response.json()["id"]

    # Récupérer la personne
    response = client.get(f"/api/v1/persons/{person_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == person_id
    assert data["last_name"] == "Lefebvre"


def test_read_person_not_found(client: TestClient):
    """Test de lecture d'une personne inexistante"""
    response = client.get("/api/v1/persons/999")
    assert response.status_code == 404


def test_update_person(client: TestClient):
    """Test de mise à jour d'une personne"""
    # Créer une personne
    create_response = client.post(
        "/api/v1/persons/",
        json={"last_name": "Durand", "first_name": "Pierre"}
    )
    person_id = create_response.json()["id"]

    # Mettre à jour la personne
    response = client.put(
        f"/api/v1/persons/{person_id}",
        json={"position": "Chef de projet"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == "Chef de projet"
    assert data["last_name"] == "Durand"  # Les autres champs sont préservés


def test_delete_person(client: TestClient):
    """Test de suppression d'une personne"""
    # Créer une personne
    create_response = client.post(
        "/api/v1/persons/",
        json={"last_name": "Bernard", "first_name": "Luc"}
    )
    person_id = create_response.json()["id"]

    # Supprimer la personne
    response = client.delete(f"/api/v1/persons/{person_id}")
    assert response.status_code == 204

    # Vérifier que la personne n'existe plus
    get_response = client.get(f"/api/v1/persons/{person_id}")
    assert get_response.status_code == 404
