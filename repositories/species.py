from sqlmodel import Session, select
from models.species import Species, SpeciesCreate, SpeciesUpdate


class SpeciesRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, conservation_status: str | None = None, offset: int = 0, limit: int = 10):
        statement = select(Species)

        if conservation_status:
            statement = statement.where(Species.conservation_status == conservation_status)

        statement = statement.offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def get_one(self, species_id: int):
        return self.session.get(Species, species_id)

    def insert(self, payload: SpeciesCreate):
        item = Species.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def update(self, species_id: int, payload: SpeciesUpdate):
        item = self.session.get(Species, species_id)
        if not item:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)

        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, species_id: int):
        item = self.session.get(Species, species_id)
        if not item:
            return False

        self.session.delete(item)
        self.session.commit()
        return True