from fastapi_utils.guid_type import GUID

from sqlalchemy.orm import relationship
from sqlalchemy import Table, String, Column, Integer, ForeignKey

from database import Base


association_table = Table(
    "association",
    Base.metadata,
    Column("classes_id", ForeignKey("classes.class_id"), primary_key=True),
    Column("students_id", ForeignKey("students.student_id"), primary_key=True),
)


class Class(Base):
    __tablename__ = "classes"

    class_id = Column(GUID, primary_key=True, index=True)
    year = Column(Integer, index=True)
    semester = Column(Integer, index=True)
    class_number = Column(Integer, index=True)

    id_user = Column(GUID, index=True)
    id_discipline = Column(GUID, index=True)

    schedules = relationship("Schedule", cascade="all, delete-orphan", passive_deletes=True)
    students = relationship(
        "Student", secondary=association_table, back_populates="classes"
    )


class Schedule(Base):
    __tablename__ = "schedules"

    schedule_id = Column(GUID, primary_key=True, index=True)
    hour = Column(String, index=True)
    week_day = Column(String, index=True, unique=True)

    class_id = Column(GUID, ForeignKey("classes.class_id", ondelete="CASCADE"), nullable=False)


class Student(Base):
    __tablename__ = "students"

    student_id = Column(GUID, primary_key=True, index=True)
    name = Column(String, index=True)
    enrollment = Column(String, index=True, unique=True)

    classes = relationship(
        "Class", secondary=association_table, back_populates="students"
    )
