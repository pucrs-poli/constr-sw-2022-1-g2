from typing import List, Union
from pydantic import BaseModel


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


class Disciplina(BaseModel):
    pass


class Usuario(BaseModel):
    pass


class Turma(TurmaCreate):
    id: int
    #alunos: List[Aluno]
    #horarios: List[Horario]
    #disciplina: Disciplina
    #usuario: Usuario

    class Config:
        orm_mode = True
