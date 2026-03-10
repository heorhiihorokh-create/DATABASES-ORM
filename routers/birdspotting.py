from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from database import get_session
from models.birdspotting import BirdspottingCreate, BirdspottingUpdate
from repositories.birdspotting import BirdspottingRepository

router = APIRouter(prefix="/birdspotting", tags=["birdspotting"])


@router.get("/")
def get_birdspottings(
    observer_name: str | None = None,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    repo = BirdspottingRepository(session)
    return repo.get_all(observer_name=observer_name, offset=offset, limit=limit)


@router.get("/{birdspotting_id}")
def get_birdspotting(birdspotting_id: int, session: Session = Depends(get_session)):
    repo = BirdspottingRepository(session)
    item = repo.get_one(birdspotting_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Birdspotting not found")
    return item


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_birdspotting(payload: BirdspottingCreate, session: Session = Depends(get_session)):
    repo = BirdspottingRepository(session)
    item = repo.insert(payload)
    if item is None:
        raise HTTPException(status_code=400, detail="Bird does not exist")
    return item


@router.put("/{birdspotting_id}")
def update_birdspotting(birdspotting_id: int, payload: BirdspottingUpdate, session: Session = Depends(get_session)):
    repo = BirdspottingRepository(session)
    item = repo.update(birdspotting_id, payload)

    if item is None:
        raise HTTPException(status_code=404, detail="Birdspotting not found")
    if item == "invalid_bird":
        raise HTTPException(status_code=400, detail="Bird does not exist")

    return item


@router.delete("/{birdspotting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_birdspotting(birdspotting_id: int, session: Session = Depends(get_session)):
    repo = BirdspottingRepository(session)
    deleted = repo.delete(birdspotting_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Birdspotting not found")
    return None