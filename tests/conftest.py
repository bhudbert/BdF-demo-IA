import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.db.session import Base, get_db
from src.main import app

# Base de données SQLite en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Fixture pour créer une session de base de données de test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Fixture pour créer un client de test"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_profile(client):
    """Fixture pour créer un profil de test"""
    profile_data = {
        "name": "Développeur Backend",
        "description": "Développeur spécialisé en API REST"
    }
    response = client.post("/api/v1/profiles/", json=profile_data)
    return response.json()


@pytest.fixture
def sample_person(client, sample_profile):
    """Fixture pour créer une personne de test"""
    person_data = {
        "last_name": "Dupont",
        "first_name": "Jean",
        "client": "Client Test",
        "client_city": "Paris",
        "position": "Développeur",
        "personal_email": "jean.dupont@example.com",
        "professional_email": "j.dupont@company.com",
        "mobile": "0601020304",
        "team": "Team A",
        "profile_id": sample_profile["id"]
    }
    response = client.post("/api/v1/persons/", json=person_data)
    return response.json()


@pytest.fixture
def sample_category(client):
    """Fixture pour créer une catégorie de test"""
    category_data = {
        "name": "Web Application",
        "description": "Applications web modernes"
    }
    response = client.post("/api/v1/categories/", json=category_data)
    return response.json()


@pytest.fixture
def sample_project(client, sample_person, sample_category):
    """Fixture pour créer un projet de test"""
    project_data = {
        "name": "Projet Test API",
        "description": "Projet de test pour l'API",
        "lead_developer_id": sample_person["id"],
        "category_id": sample_category["id"]
    }
    response = client.post("/api/v1/projects/", json=project_data)
    return response.json()


@pytest.fixture
def sample_task(client, sample_person, sample_project):
    """Fixture pour créer une tâche de test"""
    from datetime import date, timedelta
    task_data = {
        "title": "Tâche de test",
        "description": "Description de la tâche",
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=7)),
        "project_id": sample_project["id"],
        "assigned_person_id": sample_person["id"]
    }
    response = client.post("/api/v1/tasks/", json=task_data)
    return response.json()


