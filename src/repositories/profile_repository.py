"""
Repository pour le modèle Profile
"""
from src.models.profile import Profile
from src.repositories.base_repository import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
    """Repository pour les profils professionnels"""

    def __init__(self, db):
        super().__init__(Profile, db)

