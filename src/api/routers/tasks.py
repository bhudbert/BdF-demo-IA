"""
Router pour les tâches (tasks)
"""
from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.api import schemas
from src.repositories.task_repository import TaskRepository
from src.repositories.project_repository import ProjectRepository
from src.repositories.person_repository import PersonRepository
from src.db.session import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


def get_repository(db: Session = Depends(get_db)) -> TaskRepository:
    """Dépendance pour obtenir le repository"""
    return TaskRepository(db)


def get_project_repository(db: Session = Depends(get_db)) -> ProjectRepository:
    """Dépendance pour obtenir le repository Project"""
    return ProjectRepository(db)


def get_person_repository(db: Session = Depends(get_db)) -> PersonRepository:
    """Dépendance pour obtenir le repository Person"""
    return PersonRepository(db)


@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate,
    repository: TaskRepository = Depends(get_repository),
    project_repo: ProjectRepository = Depends(get_project_repository),
    person_repo: PersonRepository = Depends(get_person_repository)
):
    """Créer une nouvelle tâche"""
    # Vérifier que le projet existe
    project = project_repo.get(task.project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projet avec l'ID {task.project_id} non trouvé"
        )

    # Vérifier que la personne existe
    person = person_repo.get(task.assigned_person_id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personne avec l'ID {task.assigned_person_id} non trouvée"
        )

    # Vérifier que la date de fin est après la date de début
    if task.end_date < task.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La date de fin doit être postérieure ou égale à la date de début"
        )

    try:
        return repository.create(task.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la création: {str(e)}"
        )


@router.get("/", response_model=List[schemas.Task])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    repository: TaskRepository = Depends(get_repository)
):
    """Récupérer toutes les tâches"""
    return repository.get_all(skip=skip, limit=limit)


@router.get("/{task_id}", response_model=schemas.Task)
def read_task(
    task_id: int,
    repository: TaskRepository = Depends(get_repository)
):
    """Récupérer une tâche par son ID avec ses relations"""
    task = repository.get_with_relations(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tâche avec l'ID {task_id} non trouvée"
        )
    return task


@router.get("/by-project/{project_id}", response_model=List[schemas.Task])
def read_tasks_by_project(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    repository: TaskRepository = Depends(get_repository),
    project_repo: ProjectRepository = Depends(get_project_repository)
):
    """Récupérer toutes les tâches d'un projet"""
    # Vérifier que le projet existe
    project = project_repo.get(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projet avec l'ID {project_id} non trouvé"
        )

    return repository.get_by_project(project_id, skip=skip, limit=limit)


@router.get("/by-person/{person_id}", response_model=List[schemas.Task])
def read_tasks_by_person(
    person_id: int,
    skip: int = 0,
    limit: int = 100,
    repository: TaskRepository = Depends(get_repository),
    person_repo: PersonRepository = Depends(get_person_repository)
):
    """Récupérer toutes les tâches assignées à une personne"""
    # Vérifier que la personne existe
    person = person_repo.get(person_id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personne avec l'ID {person_id} non trouvée"
        )

    return repository.get_by_assigned_person(person_id, skip=skip, limit=limit)


@router.get("/active/", response_model=List[schemas.Task])
def read_active_tasks(
    current_date: date = Query(default=None, description="Date pour filtrer les tâches actives (par défaut: aujourd'hui)"),
    skip: int = 0,
    limit: int = 100,
    repository: TaskRepository = Depends(get_repository)
):
    """Récupérer les tâches actives à une date donnée"""
    if current_date is None:
        from datetime import date as date_module
        current_date = date_module.today()

    return repository.get_active_tasks(current_date, skip=skip, limit=limit)


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    repository: TaskRepository = Depends(get_repository),
    project_repo: ProjectRepository = Depends(get_project_repository),
    person_repo: PersonRepository = Depends(get_person_repository)
):
    """Mettre à jour une tâche"""
    # Vérifier que la tâche existe
    existing_task = repository.get(task_id)
    if existing_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tâche avec l'ID {task_id} non trouvée"
        )

    # Vérifier que le projet existe si fourni
    if task.project_id is not None:
        project = project_repo.get(task.project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Projet avec l'ID {task.project_id} non trouvé"
            )

    # Vérifier que la personne existe si fournie
    if task.assigned_person_id is not None:
        person = person_repo.get(task.assigned_person_id)
        if not person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Personne avec l'ID {task.assigned_person_id} non trouvée"
            )

    # Vérifier la cohérence des dates
    start = task.start_date if task.start_date is not None else existing_task.start_date
    end = task.end_date if task.end_date is not None else existing_task.end_date
    if end < start:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La date de fin doit être postérieure ou égale à la date de début"
        )

    try:
        updated_task = repository.update(task_id, task.model_dump(exclude_unset=True))
        if updated_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tâche avec l'ID {task_id} non trouvée"
            )
        return updated_task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la mise à jour: {str(e)}"
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    repository: TaskRepository = Depends(get_repository)
):
    """Supprimer une tâche"""
    task = repository.get(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tâche avec l'ID {task_id} non trouvée"
        )

    repository.delete(task_id)
    return None

