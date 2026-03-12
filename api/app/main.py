from datetime import datetime

from db import SessionDep, create_all_tables  # type: ignore
from fastapi import FastAPI, HTTPException, status  # type: ignore
from models import HumiditySensor, Lecture, LectureCreate
from sqlmodel import select  # type: ignore

app = FastAPI(lifespan=create_all_tables)  # type: ignore


@app.post("/sensor")
async def create_sensor(sensor_info: HumiditySensor, session: SessionDep):
    sensor = HumiditySensor.model_validate(sensor_info.model_dump())
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor


@app.get("/sensor", response_model=list[HumiditySensor])
async def list_sensors(session: SessionDep):
    humidity_sensors = session.exec(select(HumiditySensor)).all()
    return humidity_sensors


@app.delete("/sensor/{sensor_id}")
async def delete_sensor(sensor_id: int, session: SessionDep):
    sensor_db = session.get(HumiditySensor, sensor_id)
    if not sensor_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found"
        )
    session.delete(sensor_db)
    session.commit()
    return {"detail": "Sensor deleted successfully"}


@app.post("/lecture")
async def create_lecture(lecture_data: LectureCreate, session: SessionDep):
    lecture_api = lecture_data.model_dump()
    print(lecture_api.get("date_time", ()))
    lecture = Lecture(
        sensor_id=lecture_api.get("sensor_id", 0),
        lecture=lecture_api.get("lecture", 0),
        date_time=datetime(*lecture_api.get("date_time", ())),
    )
    session.add(lecture)
    session.commit()
    session.refresh(lecture)
    return lecture


@app.delete("/lecture/{sensor_id}")
async def delete_lectures(sensor_id: int, session: SessionDep):
    query = select(Lecture).where(Lecture.sensor_id == sensor_id)
    lectures_db = session.exec(query).all()
    if not lectures_db:
        return {"detail": f"No lectures for the sensor id: {sensor_id}"}
    for lecture in lectures_db:
        session.delete(lecture)
    session.commit()
    return {"detail": "All lectures deleted"}


@app.get("/lecture")
async def get_lectures(session: SessionDep):
    query = select(Lecture)
    lectures_db = session.exec(query).all()
    return lectures_db
