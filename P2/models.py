from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Turma(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, index=True)
    semestre = Column(Integer, index=True)
    num_turma = Column(Integer, index=True)
    #alunos = relationship("Aluno")
    #horarios = relationship("Horario")


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    matricula = Column(Integer, index=True)
    #turma_id = Column(Integer, ForeignKey("turmas.id"))


class Horario(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True, index=True)
    hora = Column(String, index=True)
    dia_semana = Column(Integer, index=True)
    #turma_id = Column(Integer, ForeignKey("turmas.id"))

class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
