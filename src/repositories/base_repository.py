"""
Repository de base avec les opérations CRUD génériques
"""
from typing import Generic, TypeVar, Type, List, Optional, Any, Dict
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Repository de base avec opérations CRUD génériques"""

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[ModelType]:
        """Récupérer un objet par son ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Récupérer tous les objets avec pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """Créer un nouvel objet"""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id: int, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """Mettre à jour un objet"""
        db_obj = self.get(id)
        if db_obj is None:
            return None

        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        """Supprimer un objet"""
        db_obj = self.get(id)
        if db_obj is None:
            return False

        self.db.delete(db_obj)
        self.db.commit()
        return True

    def count(self) -> int:
        """Compter le nombre total d'objets"""
        return self.db.query(self.model).count()

