from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.core.config import settings

# Création du moteur SQLAlchemy
engine = create_engine(settings.database_url)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base pour les modèles
class Base(DeclarativeBase):
    pass


def get_db():
    """Générateur de dépendance pour obtenir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
