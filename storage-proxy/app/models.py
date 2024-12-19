from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, LargeBinary
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    students = relationship("Course", back_populates="tutor")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    tutor_id = Column(Integer, ForeignKey("users.id"))
    tutor = relationship("User", back_populates="students")
    lectures = relationship("Lecture", back_populates="course")
    students = relationship("StudentLectureStats", back_populates="course")

class Lecture(Base):
    __tablename__ = "lectures"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="lectures")
    student_stats = relationship("StudentLectureStats", back_populates="lecture")

class StudentLectureStats(Base):
    __tablename__ = "student_lecture_stats"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)
    lecture_id = Column(Integer, ForeignKey("lectures.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    hand_raises = Column(Integer, default=0)
    focus_percentage = Column(Float, default=0.0)
    attendance_percentage = Column(Float, default=0.0)
    lecture = relationship("Lecture", back_populates="student_stats")
    course = relationship("Course", back_populates="students")
