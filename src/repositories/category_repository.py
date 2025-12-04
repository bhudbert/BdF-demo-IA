"""
Repository pour le modèle Category
"""
from src.models.category import Category
from src.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Repository pour les catégories"""

    def __init__(self, db):
        super().__init__(Category, db)

