from sqlalchemy.orm import Session

from . import models, schemas
from typing import Any
from fastapi import status
from fastapi.encoders import jsonable_encoder


from fastapi_utils.guid_type import GUID

########## CLASSES ##########
def set_class(db: Session, _class: schemas.Class):
    obj_in_data = jsonable_encoder(_class)
    db_class = models.Class(**obj_in_data)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def get_classes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Class).offset(skip).limit(limit).all()

def get_class_by_id(db: Session, class_id: Any):
    return db.query(models.Class).filter_by(id=class_id).first()

def delete_classes(db: Session):
    db.query(models.Class).filter().delete()
    db.commit()
    return status.HTTP_204_NO_CONTENT

def delete_class(class_id: int, db: Session):
    db.query(models.Class).filter_by(id=class_id).delete()
    db.commit()
    return status.HTTP_204_NO_CONTENT

########## STUDENTS ##########
def set_student(db: Session, student: schemas.CreateStudent):
    obj_in_data = jsonable_encoder(student)
    db_student = models.Student(**obj_in_data)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_student_by_id(db: Session, student_id: Any):
    return db.query(models.Student).filter_by(id=student_id).first()

def delete_students(db: Session):
    db.query(models.Student).filter().delete()
    db.commit()
    return status.HTTP_204_NO_CONTENT

def delete_student(db: Session, student_id: int):
    db.query(models.Student).filter_by(id=student_id).delete()
    db.commit()
    return status.HTTP_204_NO_CONTENT

########## SCHEDULES ##########
def set_schedules(db: Session, class_id: int, schedule: schemas.CreateSchedule):
    obj_in_data = jsonable_encoder(schedule)
    db_schedule = models.Schedule(**obj_in_data)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def get_schedules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Schedule).offset(skip).limit(limit).all()

def get_schedule_by_id(db: Session, schedule_id: int):
    return db.query(models.Schedule).filter_by(id=schedule_id).first()

def delete_schedules(db: Session):
    db.query(models.Schedule).filter().delete()
    db.commit()
    return status.HTTP_204_NO_CONTENT

def delete_schedule(db: Session, class_id: int, schedule_id: int):
    db.query(models.Schedule).filter_by(id=schedule_id).delete()
    db.commit()
    return status.HTTP_204_NO_CONTENT
