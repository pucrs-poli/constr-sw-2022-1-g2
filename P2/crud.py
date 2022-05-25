from sqlalchemy.orm import Session

from . import models, schemas

def get_turma_by_num_turma(db: Session, num_turma: int):
    return db.query(models.Turma).filter(models.Turma.num_turma == num_turma).first()

def create_turma(db: Session, turma: schemas.TurmaCreate):
    db_turma = models.Turma(ano=turma.ano, semestre=turma.semestre, num_turma=turma.num_turma)
    db.add(db_turma)
    db.commit()
    db.refresh(db_turma)
    return db_turma

def get_turmas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Turma).offset(skip).limit(limit).all()


def create_aluno(db: Session, aluno: schemas.AlunoCreate):
    db_aluno = models.Aluno(nome=aluno.nome, matricula=aluno.matricula)
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def get_aluno_by_matricula(db: Session, matricula: str):
    return db.query(models.Aluno).filter(models.Aluno.matricula == matricula).first()

def get_alunos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Aluno).offset(skip).limit(limit).all()


def create_horario(db: Session, horario: schemas.HorarioCreate):
    db_horario = models.Horario(hora=horario.hora, dia_semana=horario.dia_semana)
    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    return db_horario

def get_horario_by_dia_semana(db: Session, dia_semana: str):
    return db.query(models.Horario).filter(models.Horario.dia_semana == dia_semana).first()

def get_horarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Horario).offset(skip).limit(limit).all()