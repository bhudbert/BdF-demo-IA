"""
Router pour les profils professionnels
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.schemas import Profile, ProfileCreate, ProfileUpdate
from src.db.session import get_db
from src.repositories.profile_repository import ProfileRepository

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"]
)


@router.post("/", response_model=Profile, status_code=status.HTTP_201_CREATED)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    """Créer un nouveau profil"""
    repo = ProfileRepository(db)
    return repo.create(profile.model_dump())


@router.get("/", response_model=List[Profile])
def get_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtenir la liste de tous les profils"""
    repo = ProfileRepository(db)
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{profile_id}", response_model=Profile)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    """Obtenir un profil par son ID"""
    repo = ProfileRepository(db)
    profile = repo.get_by_id(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {profile_id} not found"
        )
    return profile


@router.put("/{profile_id}", response_model=Profile)
def update_profile(profile_id: int, profile: ProfileUpdate, db: Session = Depends(get_db)):
    """Mettre à jour un profil"""
    repo = ProfileRepository(db)
    updated_profile = repo.update(profile_id, profile.model_dump(exclude_unset=True))
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {profile_id} not found"
        )
    return updated_profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    """Supprimer un profil"""
    repo = ProfileRepository(db)
    success = repo.delete(profile_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {profile_id} not found"
        )

