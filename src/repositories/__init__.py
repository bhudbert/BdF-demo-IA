"""
Package repositories - Couche d'acces aux donnees (Repository pattern)
"""
from src.repositories.person_repository import PersonRepository
from src.repositories.project_repository import ProjectRepository
__all__ = ["PersonRepository", "ProjectRepository"]
