"""
Modèle Task - Représente une tâche liée à un projet et assignée à une personne
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.db.session import Base


class Task(Base):
    """Modèle pour une tâche d'un projet"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Clés étrangères
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assigned_person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)

    # Relations
    project_rel = relationship("Project", back_populates="tasks")
    assigned_person_rel = relationship("Person", back_populates="tasks")


