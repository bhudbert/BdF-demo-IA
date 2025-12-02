from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app-src.database import engine, Base
from app-src.routers import personnes, projets

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
app = FastAPI(
    title="BdF Demo IA - Carnet d'Adresses",
    description="API de gestion de personnes et de projets informatiques",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routeurs
app.include_router(personnes.router)
app.include_router(projets.router)


@app.get("/")
def read_root():
    """Endpoint racine"""
    return {
        "message": "Bienvenue sur l'API BdF Demo IA",
        "endpoints": {
            "docs": "/docs",
            "personnes": "/personnes",
            "projets": "/projets"
        }
    }


@app.get("/health")
def health_check():
    """Vérification de santé de l'API"""
    return {"status": "ok"}
