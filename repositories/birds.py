from sqlmodel import Session, select
from models.birds import Bird, BirdCreate


class BirdRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        statement = select(Bird)
        return self.session.exec(statement).all()

    def insert(self, payload: BirdCreate):
        bird = Bird.model_validate(payload)

        self.session.add(bird)
        self.session.commit()
        self.session.refresh(bird)

        return bird