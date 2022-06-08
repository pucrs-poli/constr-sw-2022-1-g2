import uuid
from typing import List
from pydantic import UUID4

from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status, Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

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
def delete_class(class_id: UUID4, db: Session = Depends(get_db)):
    tmp_class = db.query(models.Class).filter_by(id=class_id).first()
    if not tmp_class:
        raise HTTPException(status_code=404, detail="This class doesn't exists")

    db.query(models.Class).filter_by(id=class_id).delete()
    db.commit()

@app.put("/classes/{class_id}", status_code=200)
def change_class(class_id: UUID4, _class: schemas.PutClass, db: Session = Depends(get_db)):
    tmp_class = db.query(models.Class).filter_by(id=class_id).first()
    if not tmp_class:
        raise HTTPException(status_code=404, detail="This class doesn't exists")
    
    update_data = jsonable_encoder(_class)
    db.query(models.Class).filter_by(id=class_id).update(update_data)
    db.commit()

@app.patch("/classes/{class_id}", status_code=200)
def change_class_attribute(class_id: UUID4, _class: schemas.PatchClass, db: Session = Depends(get_db)):
    tmp_class = db.query(models.Class).filter_by(id=class_id).first()
    if not tmp_class:
        raise HTTPException(status_code=404, detail="This class doesn't exists")
    
    update_data = jsonable_encoder(_class)
    tmp = { key:value for key, value in update_data.items() if value }    
    db.query(models.Class).filter_by(id=class_id).update(tmp)
    db.commit()



######## SCHEDULES ##########
@app.post("/classes/{class_id}/schedules", response_model=schemas.Schedule, status_code=201)
def create_classes_schedules(class_id: UUID4, schedule: schemas.PostSchedule, db: Session = Depends(get_db)):
    _class = db.query(models.Class).filter_by(id=class_id).first()
    if not _class:
        raise HTTPException(status_code=400, detail="Can't create schedule for unexistent class")

    tmp_schedule = db.query(models.Class)\
        .join(models.Schedule)\
        .filter_by(hour=schedule.hour)\
        .filter_by(week_day=schedule.week_day)\
        .first() 
    if tmp_schedule:
        raise HTTPException(status_code=400, detail="Schedule already exists for this class")

    obj_in_data = jsonable_encoder(schedule)
    db_schedule = models.Schedule(**obj_in_data, id=uuid.uuid4())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@app.get("/classes/{class_id}/schedules", response_model=List[schemas.Schedule], status_code=200)
def retrieve_class_schedules(class_id: UUID4, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _class = db.query(models.Class).filter_by(id=class_id).first()
    if not _class:
        raise HTTPException(status_code=400, detail="Can't retrieve schedules for unexistent class")
    
    if not _class.schedules:
        raise HTTPException(status_code=400, detail="There isn't schedules for this class")
    
    schedules = db.query(models.Schedule)\
        .join(models.Class)\
        .filter_by(id=class_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return schedules

@app.delete("/classes/{class_id}/schedules", status_code=204)
def delete_class_schedules(class_id: UUID4, db: Session = Depends(get_db)):
    _class = db.query(models.Class).filter_by(id=class_id).first()
    if not _class:
        raise HTTPException(status_code=400, detail="Can't delete schedules for unexistent class")

    if not _class.schedules:
        raise HTTPException(status_code=400, detail="There isn't schedules for this class")
    
    schedules = db.query(models.Schedule)\
        .join(models.Class)\
        .filter_by(id=class_id)\
        .all()
    for schedule in schedules:
        db.delete(schedule)
    db.commit()

@app.delete("/classes/{class_id}/schedules/{schedule_id}", status_code=204)
def delete_class_schedule(class_id: UUID4, schedule_id: UUID4, db: Session = Depends(get_db)):
    _class = db.query(models.Class).filter_by(id=class_id).first()
    if not _class:
        raise HTTPException(status_code=400, detail="Can't delete schedule for unexistent class")
    
    if not _class.schedules:
        raise HTTPException(status_code=400, detail="There isn't schedules for this class")

    schedule = db.query(models.Schedule)\
        .filter_by(id=schedule_id)\
        .join(models.Class)\
        .filter_by(id=class_id)\
        .first()

    if not schedule:
        raise HTTPException(status_code=404, detail="Can't delete because this schedule doesn't exists for this class")

    db.delete(schedule)
    db.commit()

@app.put("/classes/{class_id}/schedules/{schedule_id}", status_code=200)
def change_class_schedule(class_id: UUID4, schedule_id: UUID4, schedule: schemas.PutSchedule, db: Session = Depends(get_db)):
    _class = db.query(models.Class).filter_by(id=class_id).first()
    if not _class:
        raise HTTPException(status_code=400, detail="Can't update schedule for unexistent class")
    
    if not _class.schedules:
        raise HTTPException(status_code=400, detail="There isn't schedules for this class")

    tmp_schedule = db.query(models.Schedule)\
        .filter_by(id=schedule_id)\
        .join(models.Class)\
        .filter_by(id=class_id)\
        .first()
    if not tmp_schedule:
        raise HTTPException(status_code=404, detail="Can't update because this schedule doesn't exists for this class")
    
    update_data = jsonable_encoder(schedule)
    db.query(models.Schedule)\
        .filter_by(id=tmp_schedule.id)\
        .update(update_data)
    db.commit()

@app.patch("/classes/{class_id}/schedules/{schedule_id}", status_code=200)
def change_class_schedule_attribute(class_id: UUID4, schedule_id: UUID4, schedule: schemas.PatchSchedule, db: Session = Depends(get_db)):
    _class = db.query(models.Class).filter_by(id=class_id).first()
    if not _class:
        raise HTTPException(status_code=400, detail="Can't update schedule attributes for unexistent class")
    
    if not _class.schedules:
        raise HTTPException(status_code=400, detail="There isn't schedules for this class")
    
    tmp_schedule = db.query(models.Schedule)\
        .filter_by(id=schedule_id)\
        .join(models.Class)\
        .filter_by(id=class_id)\
        .first()
    if not tmp_schedule:
        raise HTTPException(status_code=404, detail="Can't update attributes because this schedule doesn't exists for this class")
    
    update_data = jsonable_encoder(schedule)
    tmp = { key:value for key, value in update_data.items() if value }    
    db.query(models.Schedule)\
        .filter_by(id=tmp_schedule.id)\
        .update(tmp)
    db.commit()



######## STUDENTS ##########
@app.post("/students", response_model=schemas.Student, status_code=201)
def create_students(student: schemas.PostStudent, db: Session = Depends(get_db)):
    tmp_student = db.query(models.Student)\
        .filter_by(name=student.name)\
        .filter_by(enrollment=student.enrollment)\
        .first()
    if tmp_student:
        raise HTTPException(status_code=400, detail="Student already registered")
    
    obj_in_data = jsonable_encoder(student)
    db_student = models.Student(**obj_in_data, id=uuid.uuid4())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students", response_model=List[schemas.Student], status_code=200)
def retrieve_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(models.Student).\
            offset(skip).\
            limit(limit).\
            all()
    if not students:
        raise HTTPException(status_code=404, detail="There aren't registered students")
    
    return students

@app.delete("/students", status_code=204)
def delete_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).\
            filter().\
            all()
    if not students:
        raise HTTPException(status_code=400, detail="No students to delete")

    db.query(models.Student).filter().delete()
    db.commit()

@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: UUID4, db: Session = Depends(get_db)):
    student = db.query(models.Student)\
            .filter_by(id=student_id)\
            .first()
    if not student:
        raise HTTPException(status_code=404, detail="This student doesn't exists")

    db.query(models.Student).filter_by(id=student_id).delete()
    db.commit()

@app.put("/students/{student_id}", status_code=200)
def change_student(student_id: UUID4, student: schemas.PutStudent, db: Session = Depends(get_db)):
    tmp_student = db.query(models.Student)\
            .filter_by(id=student_id)\
            .first()
    if not tmp_student:
        raise HTTPException(status_code=404, detail="This student doesn't exists")

    update_data = jsonable_encoder(student)
    db.query(models.Student).filter_by(id=student_id).update(update_data)
    db.commit()

@app.patch("/students/{student_id}", status_code=200)
def change_student_attribute(student_id: UUID4, student: schemas.PatchStudent, db: Session = Depends(get_db)):
    tmp_student = db.query(models.Student)\
            .filter_by(id=student_id)\
            .first()
    if not tmp_student:
        raise HTTPException(status_code=404, detail="This student doesn't exists")

    update_data = jsonable_encoder(student)
    tmp = { key:value for key, value in update_data.items() if value }
    print(tmp)    
    db.query(models.Student).filter_by(id=student_id).update(tmp)
    db.commit()



######## CLASS STUDENTS ##########
@app.post("/classes/{class_id}/students/{student_id}", status_code=201)
def add_student_to_class(class_student: schemas.CreateClassStudents, class_id: UUID4, student_id: UUID4, db: Session = Depends(get_db)):
    obj_in_data = jsonable_encoder(class_student)
    db_class_student = models.ClassStudent(**obj_in_data)
    db.query(models.Class).filter_by(id=class_id)
    db.add(db_class_student)
    db.commit()
    db.refresh(db_class_student)
    return db_class_student

@app.delete("/classes/{class_id}/students", status_code=204)
def delete_students_from_class(class_id: UUID4):
    pass

@app.delete("/classes/{class_id}/students/{student_id}", status_code=204)
def delete_student_from_class(class_id: UUID4, student_id: UUID4):
    pass

@app.post("/students/{student_id}/classes/{class_id}", status_code=201)
def add_student_to_class(class_id: UUID4, student_id: UUID4):
    pass

@app.delete("/students/{student_id}/classes", status_code=204)
def delete_students_from_class(class_id: UUID4):
    pass

@app.delete("/students/{student_id}/classes/{class_id}", status_code=204)
def delete_student_from_class(class_id: UUID4, student_id: UUID4):
    pass
