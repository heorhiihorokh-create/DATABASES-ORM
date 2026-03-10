from sqlmodel import Session, select

from models.birdspotting import Birdspotting, BirdspottingCreate


class BirdspottingRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        statement = select(Birdspotting)
        return self.session.exec(statement).all()

    def get_one(self, birdspotting_id: int):
        statement = select(Birdspotting).where(Birdspotting.id == birdspotting_id)
        return self.session.exec(statement).first()

    def insert(self, payload: BirdspottingCreate):
        item = Birdspotting.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item