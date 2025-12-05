"""
Modèle Person - Représente une personne dans le carnet d'adresses
"""
from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from src.db.session import Base


class Person(Base):
    """Modèle pour une personne dans le carnet d'adresses"""
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    client = Column(String, nullable=True)
    client_city = Column(String, nullable=True)
    position = Column(String, nullable=True)
    personal_email = Column(String, nullable=True)
    professional_email = Column(String, nullable=True)
    landline_phone = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    team = Column(String, nullable=True)
    manager = Column(String, nullable=True)

    # Clé étrangère vers Profile
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=True)

    # Contrainte d'unicité sur le couple nom/prenom
    __table_args__ = (
        UniqueConstraint('last_name', 'first_name', name='uq_last_name_first_name'),
    )

    # Relations
    profile_rel = relationship("Profile", back_populates="persons")

    managed_projects = relationship(
        "Project",
        back_populates="project_manager_rel",
        foreign_keys="Project.project_manager_id"
    )
    dev_line_projects = relationship(
        "Project",
        back_populates="dev_line_rel",
        foreign_keys="Project.dev_line_id"
    )
    lead_developer_projects = relationship(
        "Project",
        back_populates="lead_developer_rel",
        foreign_keys="Project.lead_developer_id"
    )
    tasks = relationship("Task", back_populates="assigned_person_rel")

