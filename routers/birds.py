from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from database import get_session
from models.birds import BirdCreate, BirdUpdate
from repositories.birds import BirdRepository

router = APIRouter(prefix="/birds", tags=["birds"])


@router.get("/")
def get_birds(
    species_id: int | None = None,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    repo = BirdRepository(session)
    return repo.get_all(species_id=species_id, offset=offset, limit=limit)


@router.get("/{bird_id}")
def get_one_bird(bird_id: int, session: Session = Depends(get_session)):
    repo = BirdRepository(session)
    item = repo.get_one(bird_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Bird not found")
    return item


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_bird(payload: BirdCreate, session: Session = Depends(get_session)):
    repo = BirdRepository(session)
    item = repo.insert(payload)
    if item is None:
        raise HTTPException(status_code=400, detail="Species does not exist")
    return item


@router.put("/{bird_id}")
def update_bird(bird_id: int, payload: BirdUpdate, session: Session = Depends(get_session)):
    repo = BirdRepository(session)
    item = repo.update(bird_id, payload)

    if item is None:
        raise HTTPException(status_code=404, detail="Bird not found")
    if item == "invalid_species":
        raise HTTPException(status_code=400, detail="Species does not exist")

    return item


@router.delete("/{bird_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bird(bird_id: int, session: Session = Depends(get_session)):
    repo = BirdRepository(session)
    deleted = repo.delete(bird_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bird not found")
    return None