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
    profile_id: Optional[int] = None


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
    profile_id: Optional[int] = None


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
    category_id: Optional[int] = None


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
    category_id: Optional[int] = None


class Project(ProjectBase):
    """Schéma pour lire un projet (avec ID et relations)"""
    id: int
    project_manager_rel: Optional[Person] = None
    dev_line_rel: Optional[Person] = None
    lead_developer_rel: Optional[Person] = None

    model_config = ConfigDict(from_attributes=True)


# ========== Schémas Category ==========

class CategoryBase(BaseModel):
    """Schéma de base pour une catégorie de projet"""
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Schéma pour créer une catégorie"""
    pass


class CategoryUpdate(BaseModel):
    """Schéma pour mettre à jour une catégorie"""
    name: Optional[str] = None
    description: Optional[str] = None


class Category(CategoryBase):
    """Schéma pour lire une catégorie (avec ID)"""
    id: int

    model_config = ConfigDict(from_attributes=True)


# ========== Schémas Profile ==========

class ProfileBase(BaseModel):
    """Schéma de base pour un profil professionnel"""
    name: str
    description: Optional[str] = None


class ProfileCreate(ProfileBase):
    """Schéma pour créer un profil"""
    pass


class ProfileUpdate(BaseModel):
    """Schéma pour mettre à jour un profil"""
    name: Optional[str] = None
    description: Optional[str] = None


class Profile(ProfileBase):
    """Schéma pour lire un profil (avec ID)"""
    id: int

    model_config = ConfigDict(from_attributes=True)


