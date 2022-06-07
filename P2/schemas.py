from pydantic import BaseModel
from typing import Any, List, Optional

########## CLASSES ##########
class CreateClass(BaseModel):
    year: int
    semester: int
    class_number: int

class Class(CreateClass):
    id: Any
    students: List[Any]
    schedules: List[Any]
    #disciplina: Disciplina
    #usuario: Usuario

    class Config:
        orm_mode = True

########## STUDENTS ##########
class CreateStudent(BaseModel):
    name: str
    enrollment: str


class Student(CreateStudent):
    id: Any
    classes: List[Any]

    class Config:
        orm_mode = True

########## SCHEDULES ##########
class CreateSchedule(BaseModel):
    hour: str
    week_day: str
    class_id: Any


class Schedule(CreateSchedule):
    id: Any

    class Config:
        orm_mode = True

########## CLASS STUDENTS ##########
class CreateClassStudents(BaseModel):
    class_id: Any
    student_id: Any