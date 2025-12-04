from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api import schemas
from src.repositories.person_repository import PersonRepository
from src.db.session import get_db

router = APIRouter(
    prefix="/persons",
    tags=["persons"]
)


def get_repository(db: Session = Depends(get_db)) -> PersonRepository:
    """Dépendance pour obtenir le repository"""
    return PersonRepository(db)


@router.post("/", response_model=schemas.Person, status_code=status.HTTP_201_CREATED)
def create_person(
    person: schemas.PersonCreate,
    repository: PersonRepository = Depends(get_repository)
):
    """Créer une nouvelle personne"""
    try:
        return repository.create(person.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la création: {str(e)}"
        )


@router.get("/", response_model=List[schemas.Person])
def read_persons(
    skip: int = 0,
    limit: int = 100,
    repository: PersonRepository = Depends(get_repository)
):
    """Récupérer toutes les personnes"""
    return repository.get_all(skip=skip, limit=limit)


@router.get("/by-profile/{profile_id}", response_model=List[schemas.Person])
def read_persons_by_profile(
    profile_id: int,
    skip: int = 0,
    limit: int = 100,
    repository: PersonRepository = Depends(get_repository)
):
    """Récupérer toutes les personnes d'un profil donné"""
    persons = repository.get_by_profile(profile_id, skip=skip, limit=limit)
    return persons


@router.get("/{person_id}", response_model=schemas.Person)
def read_person(
    person_id: int,
    repository: PersonRepository = Depends(get_repository)
):
    """Récupérer une personne par son ID"""
    db_person = repository.get(person_id)
    if db_person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personne non trouvée"
        )
    return db_person


@router.put("/{person_id}", response_model=schemas.Person)
def update_person(
    person_id: int,
    person: schemas.PersonUpdate,
    repository: PersonRepository = Depends(get_repository)
):
    """Mettre à jour une personne"""
    db_person = repository.update(
        person_id,
        person.model_dump(exclude_unset=True)
    )
    if db_person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personne non trouvée"
        )
    return db_person


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(
    person_id: int,
    repository: PersonRepository = Depends(get_repository)
):
    """Supprimer une personne"""
    success = repository.delete(person_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personne non trouvée"
        )
    return None
