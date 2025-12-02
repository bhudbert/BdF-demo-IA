"""
Modèle Project - Représente un projet informatique
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.db.session import Base


class Project(Base):
    """Modèle pour un projet informatique"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Clés étrangères vers Person
    project_manager_id = Column(Integer, ForeignKey("persons.id"), nullable=True)
    dev_line_id = Column(Integer, ForeignKey("persons.id"), nullable=True)
    lead_developer_id = Column(Integer, ForeignKey("persons.id"), nullable=False)

    # Relations
    project_manager_rel = relationship(
        "Person",
        back_populates="managed_projects",
        foreign_keys=[project_manager_id]
    )
    dev_line_rel = relationship(
        "Person",
        back_populates="dev_line_projects",
        foreign_keys=[dev_line_id]
    )
    lead_developer_rel = relationship(
        "Person",
        back_populates="lead_developer_projects",
        foreign_keys=[lead_developer_id]
    )

