from typing import List
from pydantic import UUID4

from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, Response, HTTPException

from sqlalchemy.orm import Session

import crud
import models
import schemas

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return crud.set_class(db, _class)

@app.get("/classes", response_model=List[schemas.Class], status_code=200)
def get_classes(db: Session = Depends(get_db)):
    return crud.get_classes(db)

@app.get("/classes/{class_id}", response_model=schemas.Class, status_code=200)
def get_class(class_id: UUID4, db: Session = Depends(get_db)):
    return crud.get_class(db, class_id)

@app.delete("/classes", status_code=204)
def delete_classes(db: Session = Depends(get_db)):
    return crud.delete_classes(db)

@app.delete("/classes/{class_id}", status_code=204)
def delete_class(class_id: UUID4, db: Session = Depends(get_db)):
    return crud.delete_class(db, class_id)

@app.put("/classes/{class_id}", status_code=200)
def change_class(class_id: UUID4, _class: schemas.PutClass, response: Response, db: Session = Depends(get_db)):
    tmp_class: models.Class = db.query(models.Class).filter_by(class_id=class_id).one_or_none()
    if not tmp_class:
        raise HTTPException(status_code=404, detail="This class doesn't exists")

    update_data = jsonable_encoder(_class)
    db.query(models.Class).filter_by(class_id=class_id).update(update_data)
    db.commit()

@app.patch("/classes/{class_id}", status_code=204)
def change_class_attribute(class_id: UUID4, _class: schemas.PatchClass, response: Response, db: Session = Depends(get_db)):
    tmp_class = db.query(models.Class).filter_by(class_id=class_id).one_or_none()
    if not tmp_class:
        raise HTTPException(status_code=404, detail="This class doesn't exists")
    
    update_data = jsonable_encoder(_class)
    tmp = { key:value for key, value in update_data.items() if value }   
    db.query(models.Class).filter_by(class_id=class_id).update(tmp)
    db.commit()



######## STUDENTS ##########
@app.post("/students", response_model=schemas.Student, status_code=201)
def create_students(student: schemas.PostStudent, db: Session = Depends(get_db)):
    return crud.set_student(db, student)

@app.get("/students", response_model=List[schemas.Student], status_code=200)
def retrieve_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

@app.get("/students/{student_id}", response_model=schemas.Student, status_code=200)
def retrieve_student(student_id: UUID4, db: Session = Depends(get_db)):
    return crud.get_student(db, student_id)

@app.delete("/students", status_code=204)
def delete_students(db: Session = Depends(get_db)):
    crud.delete_students(db)

@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: UUID4, db: Session = Depends(get_db)):
    crud.delete_student(db, student_id)

@app.put("/students/{student_id}", status_code=200)
def change_student(student_id: UUID4, student: schemas.PutStudent, db: Session = Depends(get_db)):
    tmp_student = db.query(models.Student)\
            .filter_by(student_id=student_id)\
            .first()
    if not tmp_student:
        raise HTTPException(status_code=404, detail="This student doesn't exists")

    update_data = jsonable_encoder(student)
    db.query(models.Student).filter_by(student_id=student_id).update(update_data)
    db.commit()

@app.patch("/students/{student_id}", status_code=200)
def change_student_attribute(student_id: UUID4, student: schemas.PatchStudent, db: Session = Depends(get_db)):
    tmp_student = db.query(models.Student)\
            .filter_by(student_id=student_id)\
            .one_or_none()
    if not tmp_student:
        raise HTTPException(status_code=404, detail="This student doesn't exists")

    update_data = jsonable_encoder(student)
    tmp = { key:value for key, value in update_data.items() if value }
    db.query(models.Student).filter_by(student_id=student_id).update(tmp)
    db.commit()


######## SCHEDULES ##########
@app.post("/classes/{class_id}/schedules", response_model=schemas.Schedule, status_code=201)
def create_classes_schedules(class_id: UUID4, schedule: schemas.PostSchedule, db: Session = Depends(get_db)):
    return crud.set_schedules(db, class_id, schedule)

@app.get("/classes/{class_id}/schedules", response_model=List[schemas.Schedule], status_code=200)
def retrieve_class_schedules(class_id: UUID4, db: Session = Depends(get_db)):
    return crud.get_schedules(db, class_id)

@app.get("/classes/{class_id}/schedules/{schedule_id}", response_model=schemas.Schedule, status_code=200)
def retrieve_class_schedule(class_id: UUID4, schedule_id: UUID4, db: Session = Depends(get_db)):
    return crud.get_schedule(db, class_id, schedule_id)

@app.delete("/classes/{class_id}/schedules", status_code=204)
def delete_class_schedules(class_id: UUID4, db: Session = Depends(get_db)):
    crud.delete_schedules(db, class_id)

@app.delete("/classes/{class_id}/schedules/{schedule_id}", status_code=204)
def delete_class_schedule(class_id: UUID4, schedule_id: UUID4, db: Session = Depends(get_db)):
    crud.delete_schedule(db, class_id, schedule_id)

@app.put("/classes/{class_id}/schedules/{schedule_id}", status_code=200)
def change_class_schedule(class_id: UUID4, schedule_id: UUID4, schedule: schemas.PutSchedule, db: Session = Depends(get_db)):
    crud.change_class_schedule(db, class_id, schedule_id, schedule)

@app.patch("/classes/{class_id}/schedules/{schedule_id}", status_code=200)
def change_class_schedule_attribute(class_id: UUID4, schedule_id: UUID4, schedule: schemas.PatchSchedule, db: Session = Depends(get_db)):
    crud.change_class_schedule_attribute(db, class_id, schedule_id, schedule)



######## CLASS STUDENTS ##########
@app.post("/classes/{class_id}/students/{student_id}", status_code=200)
def add_student_to_class(class_id: UUID4, student_id: UUID4, db: Session = Depends(get_db)):
   crud.add_student_to_class(db, class_id, student_id)

@app.delete("/classes/{class_id}/students", status_code=204)
def delete_students_from_class(class_id: UUID4, db: Session = Depends(get_db)):
    crud.delete_students_from_class(db, class_id)

@app.delete("/classes/{class_id}/students/{student_id}", status_code=204)
def delete_student_from_class(class_id: UUID4, student_id: UUID4, db: Session = Depends(get_db)):
    crud.delete_student_from_class(db, class_id, student_id)

@app.post("/students/{student_id}/classes/{class_id}", status_code=201)
def add_class_to_student(student_id: UUID4, class_id: UUID4, db: Session = Depends(get_db)):
    crud.add_class_to_student(db, student_id, class_id)

@app.delete("/students/{student_id}/classes", status_code=204)
def delete_classes_from_student(student_id: UUID4, db: Session = Depends(get_db)):
    crud.delete_classes_from_student(db, student_id)

@app.delete("/students/{student_id}/classes/{class_id}", status_code=204)
def delete_class_from_student(student_id: UUID4, class_id: UUID4, db: Session = Depends(get_db)):
    crud.delete_class_from_student(db, student_id, class_id)