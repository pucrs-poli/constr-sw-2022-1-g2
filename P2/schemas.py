from pydantic import BaseModel, UUID4
from typing import Any, List, Optional

########## CLASSES ##########

class PostClass(BaseModel):
    year: int
    semester: int
    class_number: int

class PutClass(PostClass):
    id: UUID4
    
    #students: List[Any]
    #schedules: List[Any]

    id_user: UUID4
    id_discipline: UUID4

class PatchClass(BaseModel):
    id: UUID4
    year: Optional[int]
    semester: Optional[int]
    class_number: Optional[int]

    #students: Optional[List[Any]]
    #schedules: Optional[List[Any]]

    id_user: Optional[UUID4]
    id_discipline: Optional[UUID4]

class Class(PostClass):
    id: UUID4

    students: List[Any]
    schedules: List[Any]
    
    id_user: Any
    id_discipline: Any

    class Config:
        orm_mode = True

########## STUDENTS ##########
class PostStudent(BaseModel):
    name: str
    enrollment: str

class PutStudent(PostStudent):
    id: UUID4
    
    name: str
    enrollment: str
    
    #classes: List[Any]

class PatchStudent(BaseModel):
    id: UUID4
    name: Optional[str]
    enrollment: Optional[str]
    
    #classes: Optional[List[Any]]

class Student(PostStudent):
    id: UUID4
    classes: List[Any]

    class Config:
        orm_mode = True

########## SCHEDULES ##########
class PostSchedule(BaseModel):
    hour: str
    week_day: str
    
    class_id: UUID4

class PutSchedule(BaseModel):
    id: UUID4
    hour: str
    week_day: str

    #class_id: UUID4

class PatchSchedule(BaseModel):
    id: UUID4
    hour: Optional[str]
    week_day: Optional[str]
    
    #class_id: Optional[UUID4]

class Schedule(PostSchedule):
    id: UUID4

    class Config:
        orm_mode = True

########## CLASS STUDENTS ##########
class CreateClassStudents(BaseModel):
    class_id: UUID4
    student_id: UUID4