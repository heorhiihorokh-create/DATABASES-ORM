from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import Field as PydanticField


class BirdBase(SQLModel):
    nickname: str
    ring_code: str
    age: int = PydanticField(ge=0)


class Bird(BirdBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    species_id: int = Field(foreign_key="species.id")
    species: Optional["Species"] = Relationship(back_populates="birds")


class BirdCreate(BirdBase):
    species_id: int


class BirdUpdate(SQLModel):
    nickname: Optional[str] = None
    ring_code: Optional[str] = None
    age: Optional[int] = PydanticField(default=None, ge=0)
    species_id: Optional[int] = None