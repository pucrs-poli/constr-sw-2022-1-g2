from typing import List
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException

from . import crud, models, schemas
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
@app.post("/classes", response_model=schemas.Class)
def create_classes(_class: schemas.CreateClass, db: Session = Depends(get_db)):
    return crud.set_class(db=db, _class=_class)

@app.get("/classes", response_model=List[schemas.Class])
def retrieve_classes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    classes = crud.get_classes(db, skip=skip, limit=limit)
    return classes

@app.delete("/classes")
def delete_classes(db: Session = Depends(get_db)):
    return crud.delete_classes(db=db)

@app.delete("/classes/{class_id}")
def delete_class(class_id: str, db: Session = Depends(get_db)):
    return crud.delete_class(class_id=class_id, db=db)

@app.put("/classes/{class_id}")
def change_class(class_id: str):
    pass

@app.patch("/classes/{class_id}")
def change_class_attribute(class_id: str):
    pass

######## SCHEDULES ##########
@app.post("/classes/{class_id}/schedules", response_model=schemas.Schedule)
def create_classes_schedules(class_id: str, schedule: schemas.CreateSchedule, db: Session = Depends(get_db)):
    schedule = crud.set_schedules(db=db, class_id=class_id, schedule=schedule)
    return schedule

@app.get("/classes/{class_id}/schedules", response_model=List[schemas.Schedule])
def retrieve_class_schedules(class_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    schedules = crud.get_schedules(db, skip=skip, limit=limit)
    return schedules

@app.delete("/classes/{class_id}/schedules")
def delete_class_schedules(class_id: str, db: Session = Depends(get_db)):
    return crud.delete_schedules(db=db)

@app.delete("/classes/{class_id}/schedules/{schedule_id}")
def delete_class_schedule(class_id: str, schedule_id: str, db: Session = Depends(get_db)):
    return crud.delete_schedule(class_id=class_id, schedule_id=schedule_id, db=db)

@app.put("/classes/{class_id}/schedules/{schedule_id}")
def change_class_schedule(class_id: str, schedule_id: str):
    pass

@app.patch("/classes/{class_id}/schedules/{schedule_id}")
def change_class_schedule_attribute(class_id: str, schedule_id: str):
    pass

######## STUDENTS ##########
@app.post("/students", response_model=schemas.Student)
def create_students(student: schemas.CreateStudent, db: Session = Depends(get_db)):
    return crud.set_student(db=db, student=student)

@app.get("/students", response_model=List[schemas.Student])
def retrieve_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@app.delete("/students")
def delete_students(db: Session = Depends(get_db)):
    return crud.delete_students(db=db)

@app.delete("/students/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    return crud.delete_student(student_id=student_id, db=db)

@app.put("/students/{student_id}")
def change_student(student_id: str):
    pass

@app.patch("/students/{student_id}")
def change_student_attribute(student_id: str):
    pass


######## CLASS STUDENTS ##########
@app.post("/classes/{class_id}/students")
def add_students_to_class(class_id: str):
    pass

@app.post("/classes/{class_id}/students/{student_id}")
def add_student_to_class(class_id: str, student_id: str):
    pass

@app.delete("/classes/{class_id}/students")
def delete_students_from_class(class_id: str):
    pass

@app.delete("/classes/{class_id}/students/{student_id}")
def delete_student_from_class(class_id: str, student_id: str):
    pass