"""
Repository pour les opérations CRUD sur Person
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from src.models.person import Person
from src.repositories.base_repository import BaseRepository


class PersonRepository(BaseRepository[Person]):
    """Repository pour gérer les personnes"""

    def __init__(self, db: Session):
        super().__init__(Person, db)

    def get_by_last_name_first_name(self, last_name: str, first_name: str) -> Optional[Person]:
        """Récupérer une personne par nom et prénom"""
        return self.db.query(self.model).filter(
            self.model.last_name == last_name,
            self.model.first_name == first_name
        ).first()

    def search_by_name(self, search_term: str) -> List[Person]:
        """Rechercher des personnes par nom ou prénom"""
        search_pattern = f"%{search_term}%"
        return self.db.query(self.model).filter(
            (self.model.last_name.ilike(search_pattern)) |
            (self.model.first_name.ilike(search_pattern))
        ).all()

