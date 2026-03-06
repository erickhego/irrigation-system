from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

engine = create_engine("sqlite:///database.db")


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
