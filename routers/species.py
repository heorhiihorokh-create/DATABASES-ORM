from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from database import get_session
from models.species import SpeciesCreate, SpeciesUpdate
from repositories.species import SpeciesRepository

router = APIRouter(prefix="/species", tags=["species"])


@router.get("/")
def get_species(
    conservation_status: str | None = None,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    repo = SpeciesRepository(session)
    return repo.get_all(conservation_status=conservation_status, offset=offset, limit=limit)


@router.get("/{species_id}")
def get_one_species(species_id: int, session: Session = Depends(get_session)):
    repo = SpeciesRepository(session)
    item = repo.get_one(species_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Species not found")
    return item


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_species(payload: SpeciesCreate, session: Session = Depends(get_session)):
    repo = SpeciesRepository(session)
    return repo.insert(payload)


@router.put("/{species_id}")
def update_species(species_id: int, payload: SpeciesUpdate, session: Session = Depends(get_session)):
    repo = SpeciesRepository(session)
    item = repo.update(species_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail="Species not found")
    return item


@router.delete("/{species_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_species(species_id: int, session: Session = Depends(get_session)):
    repo = SpeciesRepository(session)
    deleted = repo.delete(species_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Species not found")
    return None

@router.get("/{species_id}/birds")
def get_species_birds(species_id: int, session: Session = Depends(get_session)):
    repo = SpeciesRepository(session)
    item = repo.get_one(species_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Species not found")
    return item.birds