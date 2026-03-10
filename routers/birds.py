from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from repositories.birds import BirdRepository
from models.birds import BirdCreate

router = APIRouter(prefix="/birds", tags=["birds"])


@router.get("/")
def get_birds(session: Session = Depends(get_session)):
    repo = BirdRepository(session)
    return repo.get_all()


@router.post("/")
def create_bird(payload: BirdCreate, session: Session = Depends(get_session)):
    repo = BirdRepository(session)
    return repo.insert(payload)