from .database import Base

from fastapi_utils.guid_type import GUID

from sqlalchemy.orm import relationship
from sqlalchemy import Table, String, Column, Integer, ForeignKey



class Turma(Base):
    __tablename__ = "turmas"

    id = Column(GUID, primary_key=True, index=True)
    ano = Column(Integer, index=True)
    semestre = Column(Integer, index=True)
    num_turma = Column(Integer, index=True)
    id_usuario = Column(Integer, index=True)
    id_disciplina = Column(Integer, index=True)
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


#################################################################
class ClassStudent(Base):
    __tablename__ = "classes_students"

    class_id = Column(GUID, ForeignKey("classes.id"), primary_key=True)
    student_id = Column(GUID, ForeignKey("students.id"), primary_key=True)


class Class(Base):
    __tablename__ = "classes"

    id = Column(GUID, primary_key=True, index=True)
    year = Column(Integer, index=True)
    semester = Column(Integer, index=True)
    class_number = Column(Integer, index=True)

    id_user = Column(GUID, index=True)
    id_discipline = Column(GUID, index=True)
    
    schedules = relationship("Schedule")
    students = relationship(
        "Student", secondary="ClassStudent", back_populates="classes"
    )


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(GUID, primary_key=True, index=True)
    hour = Column(String, index=True)
    week_day = Column(String, index=True)
    
    class_id = Column(GUID, ForeignKey("classes.id"))


class Student(Base):
    __tablename__ = "students"

    id = Column(GUID, primary_key=True, index=True)
    name = Column(String, index=True)
    enrollment = Column(String, index=True)
    
    classes = relationship(
        "Class", secondary="ClassStudent", back_populates="students"
    )

