from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.session import engine
from src.db.base import Base
from src.api.routers import persons, projects, tasks
from src.api.routers import categories, profiles

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
app = FastAPI(
    title="BdF Demo IA - Carnet d'Adresses",
    description="API de gestion de personnes et de projets informatiques",
    version="2.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routeurs avec le préfixe /api/v1
app.include_router(persons.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(profiles.router, prefix="/api/v1")


@app.get("/")
def read_root():
    """Endpoint racine"""
    return {
        "message": "Bienvenue sur l'API BdF Demo IA",
        "version": "2.0.0",
        "architecture": "Modulaire avec packages api/core/repositories/db/models",
        "endpoints": {
            "docs": "/docs",
            "persons": "/api/v1/persons",
            "projects": "/api/v1/projects",
            "tasks": "/api/v1/tasks",
            "categories": "/api/v1/categories",
            "profiles": "/api/v1/profiles"
        }
    }


@app.get("/health")
def health_check():
    """Vérification de santé de l'API"""
    return {"status": "ok", "version": "2.0.0"}
