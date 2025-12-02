from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app-src import crud, schemas
from app-src.database import get_db

router = APIRouter(
    prefix="/personnes",
    tags=["personnes"]
)


@router.post("/", response_model=schemas.Personne, status_code=status.HTTP_201_CREATED)
def create_personne(
    personne: schemas.PersonneCreate,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle personne"""
    try:
        return crud.create_personne(db=db, personne=personne)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la création: {str(e)}"
        )


@router.get("/", response_model=List[schemas.Personne])
def read_personnes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupérer toutes les personnes"""
    return crud.get_personnes(db=db, skip=skip, limit=limit)


@router.get("/{personne_id}", response_model=schemas.Personne)
def read_personne(
    personne_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer une personne par son ID"""
    db_personne = crud.get_personne(db=db, personne_id=personne_id)
    if db_personne is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personne non trouvée"
        )
    return db_personne


@router.put("/{personne_id}", response_model=schemas.Personne)
def update_personne(
    personne_id: int,
    personne: schemas.PersonneUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une personne"""
    db_personne = crud.update_personne(db=db, personne_id=personne_id, personne=personne)
    if db_personne is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personne non trouvée"
        )
    return db_personne


@router.delete("/{personne_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_personne(
    personne_id: int,
    db: Session = Depends(get_db)
):
    """Supprimer une personne"""
    success = crud.delete_personne(db=db, personne_id=personne_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personne non trouvée"
        )
    return None
