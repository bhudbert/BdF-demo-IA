"""
Repository pour les opérations CRUD sur Task
"""
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session, joinedload

from src.models.task import Task
from src.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """Repository pour gérer les tâches"""

    def __init__(self, db: Session):
        super().__init__(Task, db)

    def get_with_relations(self, task_id: int) -> Optional[Task]:
        """Récupérer une tâche avec toutes ses relations chargées"""
        return self.db.query(self.model).options(
            joinedload(self.model.project_rel),
            joinedload(self.model.assigned_person_rel)
        ).filter(self.model.id == task_id).first()

    def get_by_project(self, project_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """Récupérer toutes les tâches d'un projet"""
        return self.db.query(self.model).filter(
            self.model.project_id == project_id
        ).offset(skip).limit(limit).all()

    def get_by_assigned_person(self, person_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """Récupérer toutes les tâches assignées à une personne"""
        return self.db.query(self.model).filter(
            self.model.assigned_person_id == person_id
        ).offset(skip).limit(limit).all()

    def get_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> List[Task]:
        """Récupérer les tâches dans une plage de dates"""
        return self.db.query(self.model).filter(
            self.model.start_date >= start_date,
            self.model.end_date <= end_date
        ).offset(skip).limit(limit).all()

    def get_active_tasks(self, current_date: date, skip: int = 0, limit: int = 100) -> List[Task]:
        """Récupérer les tâches actives à une date donnée"""
        return self.db.query(self.model).filter(
            self.model.start_date <= current_date,
            self.model.end_date >= current_date
        ).offset(skip).limit(limit).all()

