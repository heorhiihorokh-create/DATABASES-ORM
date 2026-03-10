from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models.species import SpeciesCreate
from repositories.species import SpeciesRepository

router = APIRouter(prefix="/species", tags=["species"])


@router.get("/")
def get_species(session: Session = Depends(get_session)):
    repo = SpeciesRepository(session)
    return repo.get_all()


@router.post("/")
def create_species(payload: SpeciesCreate, session: Session = Depends(get_session)):
    repo = SpeciesRepository(session)
    return repo.insert(payload)