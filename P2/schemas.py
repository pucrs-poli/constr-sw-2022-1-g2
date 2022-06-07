from pydantic import BaseModel
from typing import Any, List, Optional


class CreateClass(BaseModel):
    year: int
    semester: int
    class_number: int


class CreateStudent(BaseModel):
    name: str
    enrollment: str


class Student(CreateStudent):
    id: int

    class Config:
        orm_mode = True


class CreateSchedule(BaseModel):
    hour: str
    week_day: str
    class_id: Any


class Schedule(CreateSchedule):
    id: int

    class Config:
        orm_mode = True


class Class(CreateClass):
    id: int
    #alunos: List[Aluno]
    schedules: List[Schedule]
    #disciplina: Disciplina
    #usuario: Usuario

    class Config:
        orm_mode = True

########## STUDENT ##########
class CreateStudentTMP(BaseModel):
    name: str
    enrollment: str


class StudentTMP(CreateStudent):
    id: int

    class Config:
        orm_mode = True


########## SCHEDULE ##########
class CreateScheduleTMP(BaseModel):
    hour: str
    week_day: str


class ScheduleTMP(CreateSchedule):
    id: int

    class Config:
        orm_mode = True


########## CLASS ##########
class ClassTmp(BaseModel):
    id: Optional[Any]
    year: int
    semester: int
    class_number: int

    id_user: Optional[Any]
    id_discipline: Optional[Any]

    students: Optional[List[Student]]
    schedules: Optional[List[Schedule]]

    class Config:
        orm_mode = True


class PatchClass(BaseModel):
    id: Any
    year: Optional[int]
    semester: Optional[int]
    class_number: Optional[int]

    id_user: Optional[Any]
    id_discipline: Optional[Any]

    students: Optional[List[Student]]
    schedules: Optional[List[Schedule]]

class PutClass(BaseModel):
    id: Any
    year: int
    semester: int
    class_number: int

    id_user: Any
    id_discipline: Any

    students: List[Student]
    schedules: List[Schedule] 