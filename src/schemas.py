from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


# ========== Schémas Personne ==========

class PersonneBase(BaseModel):
    """Schéma de base pour une personne"""
    nom: str
    prenom: str
    client: Optional[str] = None
    ville_client: Optional[str] = None
    fonction: Optional[str] = None
    email_perso: Optional[str] = None
    email_pro: Optional[str] = None
    telephone_fixe: Optional[str] = None
    mobile: Optional[str] = None
    equipe: Optional[str] = None
    responsable: Optional[str] = None


class PersonneCreate(PersonneBase):
    """Schéma pour créer une personne"""
    pass


class PersonneUpdate(BaseModel):
    """Schéma pour mettre à jour une personne"""
    nom: Optional[str] = None
    prenom: Optional[str] = None
    client: Optional[str] = None
    ville_client: Optional[str] = None
    fonction: Optional[str] = None
    email_perso: Optional[str] = None
    email_pro: Optional[str] = None
    telephone_fixe: Optional[str] = None
    mobile: Optional[str] = None
    equipe: Optional[str] = None
    responsable: Optional[str] = None


class Personne(PersonneBase):
    """Schéma pour lire une personne (avec ID)"""
    id: int

    model_config = ConfigDict(from_attributes=True)


# ========== Schémas Projet ==========

class ProjetBase(BaseModel):
    """Schéma de base pour un projet"""
    nom: str
    description: Optional[str] = None
    chef_projet_id: Optional[int] = None
    ligne_de_dev_id: Optional[int] = None
    developpeur_principal_id: int


class ProjetCreate(ProjetBase):
    """Schéma pour créer un projet"""
    pass


class ProjetUpdate(BaseModel):
    """Schéma pour mettre à jour un projet"""
    nom: Optional[str] = None
    description: Optional[str] = None
    chef_projet_id: Optional[int] = None
    ligne_de_dev_id: Optional[int] = None
    developpeur_principal_id: Optional[int] = None


class Projet(ProjetBase):
    """Schéma pour lire un projet (avec ID et relations)"""
    id: int
    chef_projet_rel: Optional[Personne] = None
    ligne_dev_rel: Optional[Personne] = None
    developpeur_principal_rel: Optional[Personne] = None

    model_config = ConfigDict(from_attributes=True)
