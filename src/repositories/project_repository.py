"""
Repository pour les opérations CRUD sur Project
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from src.models.project import Project
from src.repositories.base_repository import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """Repository pour gérer les projets"""

    def __init__(self, db: Session):
        super().__init__(Project, db)

    def get_with_relations(self, project_id: int) -> Optional[Project]:
        """Récupérer un projet avec toutes ses relations chargées"""
        return self.db.query(self.model).options(
            joinedload(self.model.project_manager_rel),
            joinedload(self.model.dev_line_rel),
            joinedload(self.model.lead_developer_rel)
        ).filter(self.model.id == project_id).first()

    def get_by_lead_developer(self, person_id: int) -> List[Project]:
        """Récupérer tous les projets d'un développeur principal"""
        return self.db.query(self.model).filter(
            self.model.lead_developer_id == person_id
        ).all()

    def get_by_project_manager(self, person_id: int) -> List[Project]:
        """Récupérer tous les projets d'un chef de projet"""
        return self.db.query(self.model).filter(
            self.model.project_manager_id == person_id
        ).all()

