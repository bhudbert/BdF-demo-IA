from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app-src.database import Base


class Personne(Base):
    """Modèle pour une personne dans le carnet d'adresses"""
    __tablename__ = "personnes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    client = Column(String, nullable=True)
    ville_client = Column(String, nullable=True)
    fonction = Column(String, nullable=True)
    email_perso = Column(String, nullable=True)
    email_pro = Column(String, nullable=True)
    telephone_fixe = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    equipe = Column(String, nullable=True)
    responsable = Column(String, nullable=True)

    # Contrainte d'unicité sur le couple nom/prenom
    __table_args__ = (
        UniqueConstraint('nom', 'prenom', name='uq_nom_prenom'),
    )

    # Relations
    projets_chef = relationship(
        "Projet",
        back_populates="chef_projet_rel",
        foreign_keys="Projet.chef_projet_id"
    )
    projets_ligne_dev = relationship(
        "Projet",
        back_populates="ligne_dev_rel",
        foreign_keys="Projet.ligne_de_dev_id"
    )
    projets_dev_principal = relationship(
        "Projet",
        back_populates="developpeur_principal_rel",
        foreign_keys="Projet.developpeur_principal_id"
    )


class Projet(Base):
    """Modèle pour un projet informatique"""
    __tablename__ = "projets"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Clés étrangères vers Personne
    chef_projet_id = Column(Integer, ForeignKey("personnes.id"), nullable=True)
    ligne_de_dev_id = Column(Integer, ForeignKey("personnes.id"), nullable=True)
    developpeur_principal_id = Column(Integer, ForeignKey("personnes.id"), nullable=False)

    # Relations
    chef_projet_rel = relationship(
        "Personne",
        back_populates="projets_chef",
        foreign_keys=[chef_projet_id]
    )
    ligne_dev_rel = relationship(
        "Personne",
        back_populates="projets_ligne_dev",
        foreign_keys=[ligne_de_dev_id]
    )
    developpeur_principal_rel = relationship(
        "Personne",
        back_populates="projets_dev_principal",
        foreign_keys=[developpeur_principal_id]
    )
