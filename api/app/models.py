from datetime import datetime

from sqlmodel import Field, SQLModel  # type: ignore


class HumiditySensor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    description: str | None = Field(default=None)


class Lecture(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="humiditysensor.id")
    lecture: int = Field(default=None)
    date_time: datetime = Field(default_factory=datetime.now(), nullable=False)


class LectureCreate(SQLModel):
    sensor_id: int
    lecture: int
    # La fecha de la lectura se mandará en una tupla de 6 enteros desde el microcontrolador
    date_time: tuple
