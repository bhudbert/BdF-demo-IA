from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app-src import crud, schemas
from app-src.database import get_db

router = APIRouter(
    prefix="/projets",
    tags=["projets"]
)


@router.post("/", response_model=schemas.Projet, status_code=status.HTTP_201_CREATED)
def create_projet(
    projet: schemas.ProjetCreate,
    db: Session = Depends(get_db)
):
    """Créer un nouveau projet"""
    # Vérifier que le développeur principal existe
    if not crud.get_personne(db, projet.developpeur_principal_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le développeur principal spécifié n'existe pas"
        )

    # Vérifier que le chef de projet existe (si spécifié)
    if projet.chef_projet_id and not crud.get_personne(db, projet.chef_projet_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le chef de projet spécifié n'existe pas"
        )

    # Vérifier que la ligne de dev existe (si spécifiée)
    if projet.ligne_de_dev_id and not crud.get_personne(db, projet.ligne_de_dev_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La ligne de dev spécifiée n'existe pas"
        )

    try:
        return crud.create_projet(db=db, projet=projet)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la création: {str(e)}"
        )


@router.get("/", response_model=List[schemas.Projet])
def read_projets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupérer tous les projets"""
    return crud.get_projets(db=db, skip=skip, limit=limit)


@router.get("/{projet_id}", response_model=schemas.Projet)
def read_projet(
    projet_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer un projet par son ID"""
    db_projet = crud.get_projet(db=db, projet_id=projet_id)
    if db_projet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    return db_projet


@router.put("/{projet_id}", response_model=schemas.Projet)
def update_projet(
    projet_id: int,
    projet: schemas.ProjetUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un projet"""
    db_projet = crud.update_projet(db=db, projet_id=projet_id, projet=projet)
    if db_projet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    return db_projet


@router.delete("/{projet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_projet(
    projet_id: int,
    db: Session = Depends(get_db)
):
    """Supprimer un projet"""
    success = crud.delete_projet(db=db, projet_id=projet_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    return None
