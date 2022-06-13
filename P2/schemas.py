from pydantic import BaseModel, UUID4
from typing import Any, List, Optional

########## CLASSES ##########

class PostClass(BaseModel):
    year: int
    semester: int
    class_number: int

    id_user: Optional[UUID4]
    id_discipline: Optional[UUID4]

    students: Optional[List[Any]] = []
    schedules: Optional[List[Any]] = []

class PutClass(PostClass):
    class_id: UUID4
    
    id_user: UUID4
    id_discipline: UUID4
    
    #students: List[Any]
    #schedules: List[Any]

class PatchClass(PutClass):
    year: Optional[int]
    semester: Optional[int]
    class_number: Optional[int]
    
    id_user: Optional[UUID4]
    id_discipline: Optional[UUID4]

    #students: Optional[List[Any]] = []
    #schedules: Optional[List[Any]] = []

class Class(PatchClass):
    students: Optional[List[Any]] = []
    schedules: Optional[List[Any]] = []
    
    class Config:
        orm_mode = True


########## STUDENTS ##########
class PostStudent(BaseModel):
    name: str
    enrollment: str

    classes: Optional[List[Any]]

class PutStudent(PostStudent):
    student_id: UUID4
    
    name: str
    enrollment: str
    
    #classes: List[Any]

class PatchStudent(PutStudent):
    name: Optional[str]
    enrollment: Optional[str]
    
    #classes: Optional[List[Any]]

class Student(PatchStudent):
    classes: Optional[List[Any]]

    class Config:
        orm_mode = True


########## SCHEDULES ##########
class PostSchedule(BaseModel):
    hour: str
    week_day: str
    
    class_id: UUID4

class PutSchedule(PostSchedule):
    schedule_id: UUID4

class PatchSchedule(PutSchedule):
    hour: Optional[str]
    week_day: Optional[str]
    
    class_id: Optional[UUID4]

class Schedule(PatchSchedule):
    class Config:
        orm_mode = True

########## CLASS STUDENTS ##########
class CreateClassStudents(BaseModel):
    class_id: UUID4
    student_id: UUID4