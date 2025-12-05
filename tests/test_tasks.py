"""
Tests pour l'API des tâches (tasks)
"""
from datetime import date, timedelta
from fastapi.testclient import TestClient


def test_create_task(client: TestClient, sample_person, sample_project):
    """Test de création d'une tâche"""
    task_data = {
        "title": "Développer API REST",
        "description": "Implémenter les endpoints CRUD",
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=7)),
        "project_id": sample_project["id"],
        "assigned_person_id": sample_person["id"]
    }

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["project_id"] == task_data["project_id"]
    assert data["assigned_person_id"] == task_data["assigned_person_id"]
    assert "id" in data


def test_read_tasks(client: TestClient, sample_task):
    """Test de lecture de toutes les tâches"""
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_read_task_by_id(client: TestClient, sample_task):
    """Test de lecture d'une tâche par son ID"""
    response = client.get(f"/api/v1/tasks/{sample_task['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_task["id"]
    assert data["title"] == sample_task["title"]


def test_read_task_not_found(client: TestClient):
    """Test de lecture d'une tâche inexistante"""
    response = client.get("/api/v1/tasks/9999")
    assert response.status_code == 404


def test_read_tasks_by_project(client: TestClient, sample_task, sample_project):
    """Test de lecture des tâches par projet"""
    response = client.get(f"/api/v1/tasks/by-project/{sample_project['id']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert all(task["project_id"] == sample_project["id"] for task in data)


def test_read_tasks_by_person(client: TestClient, sample_task, sample_person):
    """Test de lecture des tâches par personne"""
    response = client.get(f"/api/v1/tasks/by-person/{sample_person['id']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert all(task["assigned_person_id"] == sample_person["id"] for task in data)


def test_read_active_tasks(client: TestClient, sample_task):
    """Test de lecture des tâches actives"""
    response = client.get("/api/v1/tasks/active/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_task(client: TestClient, sample_task):
    """Test de mise à jour d'une tâche"""
    update_data = {
        "title": "Développer API REST v2",
        "description": "Version améliorée"
    }

    response = client.put(f"/api/v1/tasks/{sample_task['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]


def test_update_task_not_found(client: TestClient):
    """Test de mise à jour d'une tâche inexistante"""
    update_data = {"title": "Test"}
    response = client.put("/api/v1/tasks/9999", json=update_data)
    assert response.status_code == 404


def test_delete_task(client: TestClient, sample_task):
    """Test de suppression d'une tâche"""
    response = client.delete(f"/api/v1/tasks/{sample_task['id']}")
    assert response.status_code == 204

    # Vérifier que la tâche a bien été supprimée
    response = client.get(f"/api/v1/tasks/{sample_task['id']}")
    assert response.status_code == 404


def test_delete_task_not_found(client: TestClient):
    """Test de suppression d'une tâche inexistante"""
    response = client.delete("/api/v1/tasks/9999")
    assert response.status_code == 404


def test_create_task_invalid_dates(client: TestClient, sample_person, sample_project):
    """Test de création d'une tâche avec des dates invalides"""
    task_data = {
        "title": "Tâche invalide",
        "start_date": str(date.today()),
        "end_date": str(date.today() - timedelta(days=1)),  # Date de fin avant début
        "project_id": sample_project["id"],
        "assigned_person_id": sample_person["id"]
    }

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 400


def test_create_task_invalid_project(client: TestClient, sample_person):
    """Test de création d'une tâche avec un projet inexistant"""
    task_data = {
        "title": "Tâche invalide",
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=7)),
        "project_id": 9999,  # Projet inexistant
        "assigned_person_id": sample_person["id"]
    }

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 404


def test_create_task_invalid_person(client: TestClient, sample_project):
    """Test de création d'une tâche avec une personne inexistante"""
    task_data = {
        "title": "Tâche invalide",
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=7)),
        "project_id": sample_project["id"],
        "assigned_person_id": 9999  # Personne inexistante
    }

    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 404

