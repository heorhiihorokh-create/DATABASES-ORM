from sqlmodel import Session, select
from models.birds import Bird, BirdCreate, BirdUpdate
from models.species import Species


class BirdRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, species_id: int | None = None, offset: int = 0, limit: int = 10):
        statement = select(Bird)

        if species_id is not None:
            statement = statement.where(Bird.species_id == species_id)

        statement = statement.offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def get_one(self, bird_id: int):
        return self.session.get(Bird, bird_id)

    def insert(self, payload: BirdCreate):
        species = self.session.get(Species, payload.species_id)
        if species is None:
            return None

        bird = Bird.model_validate(payload)
        self.session.add(bird)
        self.session.commit()
        self.session.refresh(bird)
        return bird

    def update(self, bird_id: int, payload: BirdUpdate):
        bird = self.session.get(Bird, bird_id)
        if bird is None:
            return None

        if payload.species_id is not None:
            species = self.session.get(Species, payload.species_id)
            if species is None:
                return "invalid_species"

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(bird, key, value)

        self.session.add(bird)
        self.session.commit()
        self.session.refresh(bird)
        return bird

    def delete(self, bird_id: int):
        bird = self.session.get(Bird, bird_id)
        if bird is None:
            return False

        self.session.delete(bird)
        self.session.commit()
        return True