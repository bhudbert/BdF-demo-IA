"""
Base SQLAlchemy pour tous les modèles
"""
from src.db.session import Base

# Import tous les modèles pour que Base.metadata les connaisse
from src.models.person import Person
from src.models.project import Project

__all__ = ["Base", "Person", "Project"]

