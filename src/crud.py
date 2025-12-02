from typing import List, Optional
from sqlalchemy.orm import Session

from app-src import models, schemas


# ========== CRUD Personne ==========

def get_personne(db: Session, personne_id: int) -> Optional[models.Personne]:
    """Récupérer une personne par son ID"""
    return db.query(models.Personne).filter(models.Personne.id == personne_id).first()


def get_personnes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Personne]:
    """Récupérer toutes les personnes avec pagination"""
    return db.query(models.Personne).offset(skip).limit(limit).all()


def create_personne(db: Session, personne: schemas.PersonneCreate) -> models.Personne:
    """Créer une nouvelle personne"""
    db_personne = models.Personne(**personne.model_dump())
    db.add(db_personne)
    db.commit()
    db.refresh(db_personne)
    return db_personne


def update_personne(
    db: Session,
    personne_id: int,
    personne: schemas.PersonneUpdate
) -> Optional[models.Personne]:
    """Mettre à jour une personne"""
    db_personne = get_personne(db, personne_id)
    if db_personne is None:
        return None

    update_data = personne.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_personne, field, value)

    db.commit()
    db.refresh(db_personne)
    return db_personne


def delete_personne(db: Session, personne_id: int) -> bool:
    """Supprimer une personne"""
    db_personne = get_personne(db, personne_id)
    if db_personne is None:
        return False

    db.delete(db_personne)
    db.commit()
    return True


# ========== CRUD Projet ==========

def get_projet(db: Session, projet_id: int) -> Optional[models.Projet]:
    """Récupérer un projet par son ID"""
    return db.query(models.Projet).filter(models.Projet.id == projet_id).first()


def get_projets(db: Session, skip: int = 0, limit: int = 100) -> List[models.Projet]:
    """Récupérer tous les projets avec pagination"""
    return db.query(models.Projet).offset(skip).limit(limit).all()


def create_projet(db: Session, projet: schemas.ProjetCreate) -> models.Projet:
    """Créer un nouveau projet"""
    db_projet = models.Projet(**projet.model_dump())
    db.add(db_projet)
    db.commit()
    db.refresh(db_projet)
    return db_projet


def update_projet(
    db: Session,
    projet_id: int,
    projet: schemas.ProjetUpdate
) -> Optional[models.Projet]:
    """Mettre à jour un projet"""
    db_projet = get_projet(db, projet_id)
    if db_projet is None:
        return None

    update_data = projet.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_projet, field, value)

    db.commit()
    db.refresh(db_projet)
    return db_projet


def delete_projet(db: Session, projet_id: int) -> bool:
    """Supprimer un projet"""
    db_projet = get_projet(db, projet_id)
    if db_projet is None:
        return False

    db.delete(db_projet)
    db.commit()
    return True
