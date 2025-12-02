from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


# ========== Schémas Person ==========

class PersonBase(BaseModel):
    """Schéma de base pour une personne"""
    last_name: str
    first_name: str
    client: Optional[str] = None
    client_city: Optional[str] = None
    position: Optional[str] = None
    personal_email: Optional[str] = None
    professional_email: Optional[str] = None
    landline_phone: Optional[str] = None
    mobile: Optional[str] = None
    team: Optional[str] = None
    manager: Optional[str] = None


class PersonCreate(PersonBase):
    """Schéma pour créer une personne"""
    pass


class PersonUpdate(BaseModel):
    """Schéma pour mettre à jour une personne"""
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    client: Optional[str] = None
    client_city: Optional[str] = None
    position: Optional[str] = None
    personal_email: Optional[str] = None
    professional_email: Optional[str] = None
    landline_phone: Optional[str] = None
    mobile: Optional[str] = None
    team: Optional[str] = None
    manager: Optional[str] = None


class Person(PersonBase):
    """Schéma pour lire une personne (avec ID)"""
    id: int

    model_config = ConfigDict(from_attributes=True)


# ========== Schémas Project ==========

class ProjectBase(BaseModel):
    """Schéma de base pour un projet"""
    name: str
    description: Optional[str] = None
    project_manager_id: Optional[int] = None
    dev_line_id: Optional[int] = None
    lead_developer_id: int


class ProjectCreate(ProjectBase):
    """Schéma pour créer un projet"""
    pass


class ProjectUpdate(BaseModel):
    """Schéma pour mettre à jour un projet"""
    name: Optional[str] = None
    description: Optional[str] = None
    project_manager_id: Optional[int] = None
    dev_line_id: Optional[int] = None
    lead_developer_id: Optional[int] = None


class Project(ProjectBase):
    """Schéma pour lire un projet (avec ID et relations)"""
    id: int
    project_manager_rel: Optional[Person] = None
    dev_line_rel: Optional[Person] = None
    lead_developer_rel: Optional[Person] = None

    model_config = ConfigDict(from_attributes=True)
