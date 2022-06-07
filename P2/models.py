from .database import Base

from fastapi_utils.guid_type import GUID

from sqlalchemy.orm import relationship
from sqlalchemy import Table, String, Column, Integer, ForeignKey


#class Association(Base):
#    __tablename__ = "association"
    #class_id = Column(ForeignKey("class.id"), primary_key=True)
    #student_id = Column(ForeignKey("student.id"), primary_key=True)
    #extra_data = Column(String(50))
    #child = relationship("Class", back_populates="class")
    #parent = relationship("Student", back_populates="student")

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    semester = Column(Integer, index=True)
    class_number = Column(Integer, index=True)

    #id_user = Column(Integer, index=True)
    #id_discipline = Column(Integer, index=True)
    
    schedules = relationship("Schedule")
    #students = relationship("Association", back_populates="class")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    hour = Column(String, index=True)
    week_day = Column(String, index=True)
    
    class_id = Column(Integer, ForeignKey("classes.id"))


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    enrollment = Column(String, index=True)
    
    #classes = relationship("Association", back_populates="student")

