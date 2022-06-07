from pydantic import BaseModel
from typing import Any, List, Optional

########## CLASSES ##########

class PostClass(BaseModel):
    year: int
    semester: int
    class_number: int

class PutClass(PostClass):
    id: Any
    
    students: List[Any]
    schedules: List[Any]
    
    user_id: Any
    discipline_id: Any

class PatchClass(BaseModel):
    id: Any
    year: Optional[int]
    semester: Optional[int]
    class_number: Optional[int]
    
    students: Optional[List[Any]]
    schedules: Optional[List[Any]]

    user_id: Optional[Any]
    discipline_id: Optional[Any]

class Class(PostClass):
    id: Any

    students: List[Any]
    schedules: List[Any]
    
    user_id: Any
    discipline_id: Any

    class Config:
        orm_mode = True

########## STUDENTS ##########
class PostStudent(BaseModel):
    name: str
    enrollment: str

class PutStudent(PostStudent):
    id: Any
    
    name: str
    enrollment: str
    
    classes: List[Any]

class PatchStudent(BaseModel):
    id: Any
    name: Optional[str]
    enrollment: Optional[str]
    
    classes: Optional[List[Any]]

class Student(PostStudent):
    id: Any
    classes: List[Any]

    class Config:
        orm_mode = True

########## SCHEDULES ##########
class PostSchedule(BaseModel):
    hour: str
    week_day: str
    
    class_id: Any

class PutSchedule(PostSchedule):
    id: Any

    class_id: Any

class PatchSchedule(BaseModel):
    id: Any
    hour: Optional[str]
    week_day: Optional[str]
    
    class_id: Optional[Any]

class Schedule(PostSchedule):
    id: Any

    class Config:
        orm_mode = True

########## CLASS STUDENTS ##########
class CreateClassStudents(BaseModel):
    class_id: Any
    student_id: Any