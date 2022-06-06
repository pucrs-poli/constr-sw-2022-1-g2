from typing import List
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost", "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    item = {"Hello": "World"}
    return item


@app.post("/turmas", response_model=schemas.Turma)
def create_turmas(turma: schemas.TurmaCreate, db: Session = Depends(get_db)):
    db_turma = crud.get_turma_by_num_turma(db, num_turma=turma.num_turma)
    if db_turma:
        raise HTTPException(status_code=400, detail="Turma já existe")
    return crud.create_turma(db=db, turma=turma)

@app.get("/turmas", response_model=List[schemas.Turma])
def read_turmas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    turmas = crud.get_turmas(db, skip=skip, limit=limit)
    return turmas


@app.post("/alunos", response_model=schemas.Aluno)
def create_alunos(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    db_aluno = crud.get_aluno_by_matricula(db, matricula=aluno.matricula)
    if db_aluno:
        raise HTTPException(status_code=400, detail="Aluno já existe")
    return crud.create_aluno(db=db, aluno=aluno)

@app.get("/alunos", response_model=List[schemas.Aluno])
def read_turmas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alunos = crud.get_alunos(db, skip=skip, limit=limit)
    return alunos


@app.post("/horarios", response_model=schemas.Horario)
def create_horarios(horario: schemas.HorarioCreate, db: Session = Depends(get_db)):
    db_horario = crud.get_horario_by_dia_semana(db, dia_semana=horario.dia_semana)
    if db_horario:
        raise HTTPException(status_code=400, detail="Horário já existe")
    return crud.create_horario(db=db, horario=horario)

@app.get("/horarios", response_model=List[schemas.Horario])
def read_horarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    horarios = crud.get_horarios(db, skip=skip, limit=limit)
    return horarios

###############################################################################
@app.post("/classes", response_model=schemas.Class)
def create_classes(_class: schemas.Class, db: Session = Depends(get_db)):
    db_class = crud.get_class_by_id(db, class_id=_class.id)
    if db_class:
        raise HTTPException(status_code=400, detail="Class already exists")
    return crud.create_class(db=db, _class=_class)

######## CLASSES ##########
@app.post("/classes")
def create_classes():
    pass

@app.get("/classes")
def retrieve_classes():
    pass

@app.delete("/classes")
def delete_classes():
    pass

@app.delete("/classes/{class_id}")
def delete_class(class_id: str):
    pass

@app.put("/classes/{class_id}")
def change_class(class_id: str):
    pass

@app.patch("/classes/{class_id}")
def change_class_attribute(class_id: str):
    pass

######## SCHEDULES ##########
@app.post("/classes/{class_id}/schedules")
def create_classes_schedules(class_id: str):
    pass

@app.get("/classes/{class_id}/schedules")
def retrieve_classes_schedules(class_id: str):
    pass

@app.delete("/classes/{class_id}/schedules")
def delete_class_schedules(class_id: str):
    pass

@app.delete("/classes/{class_id}/schedules/{schedule_id}")
def delete_class_schedule(class_id: str, schedule_id: str):
    pass

@app.put("/classes/{class_id}/schedules/{schedule_id}")
def change_class_schedule(class_id: str, schedule_id: str):
    pass

@app.patch("/classes/{class_id}/schedules/{schedule_id}")
def change_class_schedule_attribute(class_id: str, schedule_id: str):
    pass

######## STUDENTS ##########
@app.post("/students")
def create_students():
    pass

@app.get("/students")
def retrieve_students():
    pass

@app.delete("/students")
def delete_students():
    pass

@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    pass

@app.put("/students/{student_id}")
def change_student(student_id: str):
    pass

@app.patch("/students/{student_id}")
def change_student_attribute(student_id: str):
    pass


######## CLASS STUDENTS ##########
@app.post("/classes/{class_id}/students")
def add_students_to_class(class_id: str):
    pass

@app.post("/classes/{class_id}/students/{student_id}")
def add_student_to_class(class_id: str, student_id: str):
    pass

@app.delete("/classes/{class_id}/students")
def delete_students_from_class(class_id: str):
    pass

@app.delete("/classes/{class_id}/students/{student_id}")
def delete_student_from_class(class_id: str, student_id: str):
    pass