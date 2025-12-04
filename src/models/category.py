"""
Modèle Category - Représente une catégorie de projet
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.db.session import Base


class Category(Base):
    """Modèle pour une catégorie de projet"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    # Relations
    projects = relationship("Project", back_populates="category_rel")

