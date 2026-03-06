from datetime import datetime

from db import SessionDep, create_all_tables  # type: ignore
from fastapi import FastAPI  # type: ignore
from models import HumiditySensor, Lecture, LectureCreate

app = FastAPI(lifespan=create_all_tables)  # type: ignore


@app.post("/sensor")
async def create_sensor(sensor_info: HumiditySensor, session: SessionDep):
    sensor = HumiditySensor.model_validate(sensor_info.model_dump())
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor


@app.post("/lecture")
async def create_lecture(lecture_data: LectureCreate, session: SessionDep):
    # breakpoint()
    lecture_api = lecture_data.model_dump()
    lecture = Lecture(
        sensor_id=lecture_api.get("sensor_id", 0),
        lecture=lecture_api.get("lecture", 0),
        date_time=datetime(*lecture_api.get("date_time", ())),
    )
    session.add(lecture)
    session.commit()
    session.refresh(lecture)
    return lecture
