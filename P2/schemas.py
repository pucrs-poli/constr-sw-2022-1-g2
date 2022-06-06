from pydantic import BaseModel
from typing import Any, List, Optional

from P2.database import Base

class TurmaCreate(BaseModel):
    ano: int
    semestre: int
    num_turma: int


class AlunoCreate(BaseModel):
    nome: str
    matricula: str


class Aluno(AlunoCreate):
    id: int

    class Config:
        orm_mode = True


class HorarioCreate(BaseModel):
    hora: str
    dia_semana: str


class Horario(HorarioCreate):
    id: int

    class Config:
        orm_mode = True


class Turma(TurmaCreate):
    id: int
    #alunos: List[Aluno]
    #horarios: List[Horario]
    #disciplina: Disciplina
    #usuario: Usuario

    class Config:
        orm_mode = True

#############################################################

########## STUDENT ##########
class CreateStudent(BaseModel):
    name: str
    enrollment: str


class Student(CreateStudent):
    id: int

    class Config:
        orm_mode = True


########## SCHEDULE ##########
class CreateSchedule(BaseModel):
    hour: str
    week_day: str


class Schedule(CreateSchedule):
    id: int

    class Config:
        orm_mode = True


########## CLASS ##########
class Class(BaseModel):
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


class PatchClass(Base):
    id: Any
    year: Optional[int]
    semester: Optional[int]
    class_number: Optional[int]

    id_user: Optional[Any]
    id_discipline: Optional[Any]

    students: Optional[List[Student]]
    schedules: Optional[List[Schedule]]

class PutClass(Base):
    id: Any
    year: int
    semester: int
    class_number: int

    id_user: Any
    id_discipline: Any

    students: List[Student]
    schedules: List[Schedule] 