from .database import Base

from fastapi_utils.guid_type import GUID

from sqlalchemy.orm import relationship
from sqlalchemy import Table, String, Column, Integer, ForeignKey

'''
class ClassStudent(Base):
    __tablename__ = "classes_students"

    class_id = Column(ForeignKey("classes.id"), primary_key=True)
    student_id = Column(ForeignKey("students.id"), primary_key=True)

    _class = relationship("Class", back_populates="students")
    students = relationship("Student", back_populates="classes")
'''
association_table = Table(
    "association",
    Base.metadata,
    Column("classes_id", ForeignKey("classes.id"), primary_key=True),
    Column("students_id", ForeignKey("students.id"), primary_key=True),
)

class Class(Base):
    __tablename__ = "classes"

    id = Column(GUID, primary_key=True, index=True)
    year = Column(Integer, index=True)
    semester = Column(Integer, index=True)
    class_number = Column(Integer, index=True)

    id_user = Column(GUID, index=True)
    id_discipline = Column(GUID, index=True)

    schedules = relationship(
        "Schedule", cascade="all, delete, delete-orphan", passive_deletes=True
    )
    students = relationship(
        "Student", secondary=association_table, back_populates="classes"
    )


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(GUID, primary_key=True, index=True)
    hour = Column(String, index=True)
    week_day = Column(String, index=True)

    class_id = Column(GUID, ForeignKey("classes.id", ondelete="CASCADE"))


class Student(Base):
    __tablename__ = "students"

    id = Column(GUID, primary_key=True, index=True)
    name = Column(String, index=True)
    enrollment = Column(String, index=True)

    classes = relationship(
        "Class", secondary=association_table, back_populates="students"
    )

