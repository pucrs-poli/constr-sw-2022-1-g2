from uuid import uuid4
from pydantic import UUID4
from sqlalchemy.orm import Session

import models
import schemas

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder


########## CLASSES ##########
def set_class(db: Session, _class: schemas.PostClass):
    aux_class = \
        db.query(models.Class)\
        .filter_by(year=_class.year)\
        .filter_by(semester=_class.semester)\
        .filter_by(class_number=_class.class_number)\
        .first()

    if aux_class:
        raise HTTPException(status_code=400, detail="The class already exists")

    db_class = models.Class(
        class_id=uuid4(),
        year=_class.year,
        id_user=_class.id_user,
        semester=_class.semester,
        class_number=_class.class_number,
        id_discipline=_class.id_discipline,
    )

    if _class.students:
        for student in _class.students:
            aux_student = \
                db.query(models.Student)\
                .filter_by(enrollment=student.get("enrollment"))\
                .first()
            if aux_student:
                db_class.students.append(aux_student)
            else:
                db_student = models.Student(
                    student_id=uuid4(),
                    name=student.get("name"),
                    enrollment=student.get("enrollment")
                )
                db_class.students.append(db_student)
    
    if _class.schedules:
        for schedule in _class.schedules:
            aux_schedule = db.query(models.Schedule)\
                .filter_by(hour=schedule.get("hour"))\
                .filter_by(week_day=schedule.get("week_day"))\
                .first()
            if aux_schedule:
                db_class.schedules.append(aux_schedule)
            else:
                db_schedule = models.Schedule(
                    schedule_id=uuid4(),
                    hour=schedule.get("hour"),
                    week_day=schedule.get("week_day"),
                )
                db_class.schedules.append(db_schedule)

    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def get_classes(db: Session):
    classes = \
        db.query(models.Class).\
        filter().\
        all()

    if not classes:
        raise HTTPException(status_code=404, detail="There aren't registered classes")

    return classes

def get_class(db: Session, class_id: UUID4):
    _class = \
        db.query(models.Class)\
        .filter_by(class_id=class_id)\
        .first()

    if not _class:
        raise HTTPException(status_code=404, detail="The class isn't registered")

    return _class

def delete_classes(db: Session):
    classes = \
        db.query(models.Class).\
        filter().\
        all()

    if not classes:
        raise HTTPException(status_code=400, detail="There aren't classes to delete")
    
    for _class in classes:
        if _class.students:
            _class.students.clear()
        
        if _class.schedules:
            _class.schedules.clear()

        db.delete(_class)

    db.commit()

def delete_class(db: Session, class_id: int):
    _class = \
        db.query(models.Class)\
        .filter_by(class_id=class_id)\
        .first()
    if not _class:
        raise HTTPException(status_code=404, detail="The class isn't registered")    

    if _class.students:
        _class.students.clear()
        
    if _class.schedules:
        _class.schedules.clear()

    db.delete(_class)
    db.commit()

def change_class(db: Session, class_id: UUID4, _class: schemas.PutClass):
    pass

def change_class_attribute(db: Session, class_id: UUID4, _class: schemas.PatchClass):
    pass




########## STUDENTS ##########
def set_student(db: Session, student: schemas.PostStudent):
    aux_student = \
        db.query(models.Student)\
        .filter_by(enrollment=student.enrollment)\
        .first()
    if aux_student:
        raise HTTPException(status_code=400, detail="Student already registered")

    db_student = models.Student(
        name=student.name,
        student_id=uuid4(),
        enrollment=student.enrollment,
    )

    if student.classes:
        for _class in student.classes:

            aux_class = \
                db.query(models.Class)\
                .filter_by(year=_class.get("year"))\
                .filter_by(semester=_class.get("semester"))\
                .filter_by(class_number=_class.get("class_number"))\
                .first()

            if aux_class:
                db_student.classes.append(aux_class)

            else:
                db_class = models.Class(
                    class_id=uuid4(),
                    year=_class.get("year"),
                    semester=_class.get("semester"),
                    class_number=_class.get("class_number"),
                    id_user=_class.get("id_user"),
                    id_discipline=_class.get("id_discipline"),
                )
                
                if _class.get("schedules", False):
                    for schedule in _class["schedules"]:
                        db_schedule = models.Schedule(
                            hour=schedule.get("hour"),
                            schedule_id=uuid4(),
                            week_day=schedule.get("week_day"),
                        )
                        db_class.schedules.append(db_schedule)
                
                db_student.classes.append(db_class)

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_students(db: Session):
    students = db.query(models.Student).\
            filter().\
            all()
    if not students:
        raise HTTPException(status_code=404, detail="There aren't enrolled students")
    
    return students

def get_student(db: Session, student_id: UUID4):
    student = \
        db.query(models.Student).\
        filter_by(student_id=student_id).\
        first()
    if not student:
        raise HTTPException(status_code=404, detail="The student isn't enrolled")
    
    return student

def delete_students(db: Session):
    students = db.query(models.Student).\
            filter().\
            all()
    if not students:
        raise HTTPException(status_code=404, detail="There aren't enrolled students")

    for student in students:
        db.delete(student)
    
    db.commit()
        
def delete_student(db: Session, student_id: UUID4):
    student = \
        db.query(models.Student)\
        .filter_by(student_id=student_id)\
        .first()
    if not student:
        raise HTTPException(status_code=404, detail="The student isn't enrolled")

    db.delete(student)
    db.commit()

def change_student(db: Session, student_id: UUID4, student: schemas.PutStudent):
    pass

def change_student_attribute(db: Session, student_id: UUID4, student: schemas.PatchStudent):
    pass



########## SCHEDULES ##########
def set_schedules(db: Session, class_id: UUID4, schedule: schemas.PostSchedule):
    _class = \
        db.query(models.Class)\
        .filter_by(class_id=class_id)\
        .first()
    
    if not _class:
        raise HTTPException(status_code=400, detail="Can't create schedule for unexistent class")

    aux_schedule = db.query(models.Class)\
        .join(models.Schedule)\
        .filter_by(hour=schedule.hour)\
        .filter_by(week_day=schedule.week_day)\
        .first()
    
    if aux_schedule:
        raise HTTPException(status_code=400, detail="Schedule already exists for this class")

    schedule_id = uuid4()

    obj_in_data = jsonable_encoder(schedule)
    db_schedule = models.Schedule(
        **obj_in_data,
        schedule_id=schedule_id
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def get_schedules(db: Session, class_id: UUID4):
    _class = \
        db.query(models.Class)\
        .filter_by(class_id=class_id)\
        .first()

    if not _class:
        raise HTTPException(status_code=400, detail="Can't retrieve schedules for unexistent class")
    
    if not _class.schedules:
        raise HTTPException(status_code=400, detail="There aren't schedules for this class")
    
    return _class.schedules

def get_schedule(db: Session, class_id: UUID4, schedule_id: UUID4):
    _class = \
        db.query(models.Class)\
        .filter_by(class_id=class_id)\
        .first()
    
    if not _class:
        raise HTTPException(status_code=400, detail="Can't retrieve schedules for unexistent class")
    
    if not _class.schedules:
        raise HTTPException(status_code=400, detail="There isn't schedules for this class")
    
    for schedule in _class.schedules:
        if schedule.schedule_id == schedule_id:
            return schedule
    else:
        raise HTTPException(status_code=400, detail="Can't get this schedule because it doesn't exists for this class")

def delete_schedules(db: Session, class_id: UUID4):
    _class = \
        db.query(models.Class)\
        .filter_by(class_id=class_id)\
        .first()
    
    if not _class:
        raise HTTPException(status_code=400, detail="Can't delete schedules for unexistent class")

    if not _class.schedules:
        raise HTTPException(status_code=400, detail="There aren't schedules for this class")
    
    _class.schedules.clear()
    db.commit()

def delete_schedule(db: Session, class_id: UUID4, schedule_id: UUID4):
    _class = \
        db.query(models.Class)\
        .filter_by(class_id=class_id)\
        .first()
    
    if not _class:
        raise HTTPException(status_code=400, detail="Can't delete schedule for unexistent class")
    
    if not _class.schedules:
        raise HTTPException(status_code=400, detail="There isn't schedules for this class")

    for schedule in _class.schedules:
        if schedule.schedule_id == schedule_id:
            _class.schedules.remove(schedule)
            db.commit()
            break
    else:
        raise HTTPException(status_code=404, detail="Can't delete because this schedule doesn't exists for this class")

def change_class_schedule(db: Session, class_id: UUID4, schedule_id: UUID4, schedule: schemas.PutSchedule):
    _class = db.query(models.Class).filter_by(class_id=class_id).one_or_none()
    
    if not _class:
        raise HTTPException(status_code=400, detail="Can't update schedule for unexistent class")
    
    if not _class.schedules:
        raise HTTPException(status_code=400, detail="There isn't schedules for this class")

    tmp_schedule = db.query(models.Schedule)\
        .filter_by(schedule_id=schedule_id)\
        .join(models.Class)\
        .filter_by(class_id=class_id)\
        .one_or_none()
    
    if not tmp_schedule:
        raise HTTPException(status_code=404, detail="Can't update because this schedule doesn't exists for this class")
    
    update_data = jsonable_encoder(schedule)
    db.query(models.Schedule)\
        .filter_by(schedule_id=tmp_schedule.schedule_id)\
        .update(update_data)
    db.commit()

def change_class_schedule_attribute(db: Session, class_id: UUID4, schedule_id: UUID4, schedule: schemas.PatchSchedule):
    _class = db.query(models.Class).filter_by(class_id=class_id).one_or_none()
    if not _class:
        raise HTTPException(status_code=400, detail="Can't update schedule attributes for unexistent class")
    
    if not _class.schedules:
        raise HTTPException(status_code=400, detail="There isn't schedules for this class")
    
    tmp_schedule = db.query(models.Schedule)\
        .filter_by(schedule_id=schedule_id)\
        .join(models.Class)\
        .filter_by(class_id=class_id)\
        .one_or_none()
    if not tmp_schedule:
        raise HTTPException(status_code=404, detail="Can't update attributes because this schedule doesn't exists for this class")
    
    update_data = jsonable_encoder(schedule)
    tmp = { key:value for key, value in update_data.items() if value }    
    db.query(models.Schedule)\
        .filter_by(schedule_id=tmp_schedule.schedule_id)\
        .update(tmp)
    db.commit()


########## CLASS STUDENTS ##########
def add_student_to_class(db: Session, class_id: UUID4, student_id: UUID4):
    _class = db.query(models.Class).filter_by(class_id=class_id).one_or_none()
    if not _class:
        raise HTTPException(status_code=404, detail="This class doesn't exists")
    
    student = db.query(models.Student).filter_by(student_id=student_id).one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="This student doesn't exists")
    
    if student in _class.students:
        raise HTTPException(status_code=400, detail="Student already enrolled for this class")
    
    _class.students.append(student)
    db.commit()

def delete_students_from_class(db: Session, class_id: UUID4):
    _class = db.query(models.Class).filter_by(class_id=class_id).one_or_none()
    if not _class:
        raise HTTPException(status_code=404, detail="This class doesn't exists")
    
    if not _class.students:
        raise HTTPException(status_code=400, detail="This class doesn't have students")

    _class.students.clear()
    db.commit()

def delete_student_from_class(db: Session, class_id: UUID4, student_id: UUID4):
    _class = db.query(models.Class).filter_by(class_id=class_id).one_or_none()
    if not _class:
        raise HTTPException(status_code=404, detail="This class doesn't exists")
    
    student = db.query(models.Student).filter_by(student_id=student_id).one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="This student doesn't exists")

    if not student in _class.students:
        raise HTTPException(status_code=400, detail="The student isn't enrolled for this class")

    _class.students.remove(student)
    db.commit()

def add_class_to_student(db: Session, student_id: UUID4, class_id: UUID4):
    student = db.query(models.Student).filter_by(student_id=student_id).one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="This student doesn't exists")

    _class = db.query(models.Class).filter_by(class_id=class_id).one_or_none()
    if not _class:
        raise HTTPException(status_code=404, detail="This class doesn't exists")
    
    if _class in student.classes:
        raise HTTPException(status_code=400, detail="Student already enrolled for this class")
    
    student.classes.append(_class)
    db.commit()

def delete_classes_from_student(db: Session, student_id: UUID4):
    student = db.query(models.Student).filter_by(student_id=student_id).one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="This student doesn't exists")
    
    if not student.classes:
        raise HTTPException(status_code=400, detail="This students isn't enrolled in any classes")

    student.classes.clear()
    db.commit()

def delete_class_from_student(db: Session, student_id: UUID4, class_id: UUID4):
    student = db.query(models.Student).filter_by(student_id=student_id).one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="This student doesn't exists")

    _class = db.query(models.Class).filter_by(class_id=class_id).one_or_none()
    if not _class:
        raise HTTPException(status_code=404, detail="This class doesn't exists")

    if not _class in student.classes:
        raise HTTPException(status_code=400, detail="The student isn't enrolled for this class")

    student.classes.remove(_class)
    db.commit()
