"""
Router pour les catégories de projets
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.schemas import Category, CategoryCreate, CategoryUpdate
from src.db.session import get_db
from src.repositories.category_repository import CategoryRepository

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle catégorie"""
    repo = CategoryRepository(db)
    return repo.create(category.model_dump())


@router.get("/", response_model=List[Category])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtenir la liste de toutes les catégories"""
    repo = CategoryRepository(db)
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Obtenir une catégorie par son ID"""
    repo = CategoryRepository(db)
    category = repo.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    return category


@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    """Mettre à jour une catégorie"""
    repo = CategoryRepository(db)
    updated_category = repo.update(category_id, category.model_dump(exclude_unset=True))
    if not updated_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    return updated_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Supprimer une catégorie"""
    repo = CategoryRepository(db)
    success = repo.delete(category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )

