from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

###############################################################################

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