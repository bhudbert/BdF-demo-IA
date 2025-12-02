from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api import schemas
from src.repositories.project_repository import ProjectRepository
from src.repositories.person_repository import PersonRepository
from src.db.session import get_db

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)


def get_project_repository(db: Session = Depends(get_db)) -> ProjectRepository:
    """Dépendance pour obtenir le repository project"""
    return ProjectRepository(db)


def get_person_repository(db: Session = Depends(get_db)) -> PersonRepository:
    """Dépendance pour obtenir le repository person"""
    return PersonRepository(db)


@router.post("/", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project: schemas.ProjectCreate,
    project_repo: ProjectRepository = Depends(get_project_repository),
    person_repo: PersonRepository = Depends(get_person_repository)
):
    """Créer un nouveau projet"""
    # Vérifier que le développeur principal existe
    if not person_repo.get(project.lead_developer_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le développeur principal spécifié n'existe pas"
        )

    # Vérifier que le chef de projet existe (si spécifié)
    if project.project_manager_id and not person_repo.get(project.project_manager_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le chef de projet spécifié n'existe pas"
        )

    # Vérifier que la ligne de dev existe (si spécifiée)
    if project.dev_line_id and not person_repo.get(project.dev_line_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La ligne de dev spécifiée n'existe pas"
        )

    try:
        return project_repo.create(project.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la création: {str(e)}"
        )


@router.get("/", response_model=List[schemas.Project])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    repository: ProjectRepository = Depends(get_project_repository)
):
    """Récupérer tous les projets"""
    return repository.get_all(skip=skip, limit=limit)


@router.get("/{project_id}", response_model=schemas.Project)
def read_project(
    project_id: int,
    repository: ProjectRepository = Depends(get_project_repository)
):
    """Récupérer un projet par son ID"""
    db_project = repository.get(project_id)
    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    return db_project


@router.put("/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int,
    project: schemas.ProjectUpdate,
    repository: ProjectRepository = Depends(get_project_repository)
):
    """Mettre à jour un projet"""
    db_project = repository.update(
        project_id,
        project.model_dump(exclude_unset=True)
    )
    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    return db_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    repository: ProjectRepository = Depends(get_project_repository)
):
    """Supprimer un projet"""
    success = repository.delete(project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    return None
