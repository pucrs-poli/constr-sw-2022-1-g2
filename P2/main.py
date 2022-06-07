from typing import Any, List
import uuid

from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware
from fastapi import status, Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost", "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    item = {"Hello": "World"}
    return item


######## CLASSES ##########
@app.post("/classes", response_model=schemas.Class, status_code=201)
def create_classes(_class: schemas.PostClass, db: Session = Depends(get_db)):
    tmp_class = db.query(models.Class)\
        .filter_by(
            year=_class.year,
            semester=_class.semester, 
            class_number=_class.class_number
        )\
        .first()
    if tmp_class:
        raise HTTPException(status_code=400, detail="Class already registered")
    
    obj_in_data = jsonable_encoder(_class)
    db_class = models.Class(**obj_in_data, id=uuid.uuid4())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

@app.get("/classes", response_model=List[schemas.Class], status_code=200)
def get_classes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    classes = db.query(models.Class).\
            offset(skip).\
            limit(limit).\
            all()
    if not classes:
        raise HTTPException(status_code=404, detail="There aren't registered classes")
    return classes

@app.delete("/classes", status_code=204)
def delete_classes(db: Session = Depends(get_db)):
    classes = db.query(models.Class).\
            filter().\
            all()
    if not classes:
        raise HTTPException(status_code=400, detail="No classes to delete")
    db.query(models.Class).filter().delete()
    db.commit()

@app.delete("/classes/{class_id}", status_code=204)
def delete_class(class_id: str, db: Session = Depends(get_db)):
    _class = db.query(models.Class).filter_by(id=class_id).first()
    if not _class:
        raise HTTPException(status_code=400, detail="This class doesn't exists")

    db.query(models.Class).filter_by(id=class_id).delete()
    db.commit()

@app.put("/classes/{class_id}", status_code=200)
def change_class(class_id: str):
    pass

@app.patch("/classes/{class_id}", status_code=200)
def change_class_attribute(class_id: str):
    pass

######## SCHEDULES ##########
@app.post("/classes/{class_id}/schedules", response_model=schemas.Schedule, status_code=201)
def create_classes_schedules(class_id:int, schedule: schemas.PostSchedule, db: Session = Depends(get_db)):
    _class = db.query(models.Class).filter_by(id=class_id).first()
    if not _class:
        raise HTTPException(status_code=400, detail="Can't create schedule for unexistent class")

    tmp_schedule = db.query(models.Schedule)\
        .join(models.Class)\
        .filter_by(
            hour=schedule.hour,
            week_day=schedule.week_day
        )\
        .fist()
    if tmp_schedule:
        raise HTTPException(status_code=400, detail="Schedule already exists for this class")

    obj_in_data = jsonable_encoder(schedule)
    db_schedule = models.Schedule(**obj_in_data)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@app.get("/classes/{class_id}/schedules", response_model=List[schemas.Schedule], status_code=200)
def retrieve_class_schedules(class_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # what if class doesn't exists?
    # what if there isn't schedules for that class?
    schedules = db.query(models.Schedule)\
        .join(models.Class)\
        .filter_by(id=class_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return schedules

@app.delete("/classes/{class_id}/schedules", status_code=204)
def delete_class_schedules(class_id: str, db: Session = Depends(get_db)):
    # what if class doesn't exists?
    # what if there isn't schedules for that class?
    schedules = db.query(models.Schedule)\
        .join(models.Class)\
        .filter_by(id=class_id)\
        .all()
    for schedule in schedules:
        db.delete(schedule)
    db.commit()
    return status.HTTP_204_NO_CONTENT

@app.delete("/classes/{class_id}/schedules/{schedule_id}", status_code=204)
def delete_class_schedule(class_id: str, schedule_id: str, db: Session = Depends(get_db)):
    # what if class doesn't exists?
    # what if there isn't schedules for that class?
    schedule = db.query(models.Schedule)\
        .join(models.Class)\
        .filter_by(id=class_id)\
        .filter_by(id=schedule_id)\
        .first()
    db.delete(schedule)
    db.commit()
    return status.HTTP_204_NO_CONTENT

@app.put("/classes/{class_id}/schedules/{schedule_id}", status_code=200)
def change_class_schedule(class_id: str, schedule_id: str):
    pass

@app.patch("/classes/{class_id}/schedules/{schedule_id}")
def change_class_schedule_attribute(class_id: str, schedule_id: str, status_code=200):
    pass

######## STUDENTS ##########
@app.post("/students", response_model=schemas.Student, status_code=201)
def create_students(student: schemas.PostStudent, db: Session = Depends(get_db)):
    obj_in_data = jsonable_encoder(student)
    db_student = models.Student(**obj_in_data)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students", response_model=List[schemas.Student], status_code=200)
def retrieve_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Student).\
            offset(skip).\
            limit(limit).\
            all()

@app.delete("/students", status_code=204)
def delete_students(db: Session = Depends(get_db)):
    db.query(models.Student).filter().delete()
    db.commit()
    return status.HTTP_204_NO_CONTENT

@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    db.query(models.Student).filter_by(id=student_id).delete()
    db.commit()
    return status.HTTP_204_NO_CONTENT

@app.put("/students/{student_id}", status_code=200)
def change_student(student_id: str):
    pass

@app.patch("/students/{student_id}", status_code=200)
def change_student_attribute(student_id: str):
    pass


######## CLASS STUDENTS ##########
@app.post("/classes/{class_id}/students/{student_id}", status_code=201)
def add_student_to_class(class_student: schemas.CreateClassStudents, class_id: str, student_id: str, db: Session = Depends(get_db)):
    obj_in_data = jsonable_encoder(class_student)
    db_class_student = models.ClassStudent(**obj_in_data)
    db.query(models.Class).filter_by(id=class_id)
    db.add(db_class_student)
    db.commit()
    db.refresh(db_class_student)
    return db_class_student

@app.delete("/classes/{class_id}/students", status_code=204)
def delete_students_from_class(class_id: str):
    pass

@app.delete("/classes/{class_id}/students/{student_id}", status_code=204)
def delete_student_from_class(class_id: str, student_id: str):
    pass

@app.post("/students/{student_id}/classes/{class_id}", status_code=201)
def add_student_to_class(class_id: str, student_id: str):
    pass

@app.delete("/students/{student_id}/classes", status_code=204)
def delete_students_from_class(class_id: str):
    pass

@app.delete("/students/{student_id}/classes/{class_id}", status_code=204)
def delete_student_from_class(class_id: str, student_id: str):
    pass
