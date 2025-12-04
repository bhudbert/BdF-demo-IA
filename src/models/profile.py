"""
Modèle Profile - Représente un profil professionnel (type de fonction)
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.db.session import Base


class Profile(Base):
    """Modèle pour un profil professionnel (Développeur, DevOps, Chef de projet, etc.)"""
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    # Relations
    persons = relationship("Person", back_populates="profile_rel")

