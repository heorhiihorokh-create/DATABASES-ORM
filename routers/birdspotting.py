from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database import get_session
from models.birdspotting import BirdspottingCreate
from repositories.birdspotting import BirdspottingRepository

router = APIRouter(prefix="/birdspotting", tags=["birdspotting"])


@router.get("/")
def get_birdspottings(session: Session = Depends(get_session)):
    repo = BirdspottingRepository(session)
    return repo.get_all()


@router.get("/{birdspotting_id}")
def get_birdspotting(birdspotting_id: int, session: Session = Depends(get_session)):
    repo = BirdspottingRepository(session)
    item = repo.get_one(birdspotting_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Birdspotting not found")

    return item


@router.post("/")
def create_birdspotting(payload: BirdspottingCreate, session: Session = Depends(get_session)):
    repo = BirdspottingRepository(session)
    return repo.insert(payload)