from sqlmodel import Session, select
from models.birdspotting import Birdspotting, BirdspottingCreate, BirdspottingUpdate
from models.birds import Bird


class BirdspottingRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, observer_name: str | None = None, offset: int = 0, limit: int = 10):
        statement = select(Birdspotting)

        if observer_name:
            statement = statement.where(Birdspotting.observer_name == observer_name)

        statement = statement.offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def get_one(self, birdspotting_id: int):
        return self.session.get(Birdspotting, birdspotting_id)

    def insert(self, payload: BirdspottingCreate):
        bird = self.session.get(Bird, payload.bird_id)
        if bird is None:
            return None

        item = Birdspotting.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def update(self, birdspotting_id: int, payload: BirdspottingUpdate):
        item = self.session.get(Birdspotting, birdspotting_id)
        if item is None:
            return None

        if payload.bird_id is not None:
            bird = self.session.get(Bird, payload.bird_id)
            if bird is None:
                return "invalid_bird"

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)

        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, birdspotting_id: int):
        item = self.session.get(Birdspotting, birdspotting_id)
        if item is None:
            return False

        self.session.delete(item)
        self.session.commit()
        return True