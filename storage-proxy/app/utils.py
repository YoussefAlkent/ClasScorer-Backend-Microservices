from sqlalchemy.orm import Session
from app.models import User, Course, Lecture
from app.hashing import hash_password

def create_user(db: Session, username: str, email: str, password: str):
    hashed_password = hash_password(password)
    user = User(username=username, email=email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def register_course(db: Session, name: str, description: str, tutor_id: int):
    course = Course(name=name, description=description, tutor_id=tutor_id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def create_lecture(db: Session, course_id: int, start_time: str, end_time: str):
    lecture = Lecture(course_id=course_id, start_time=start_time, end_time=end_time)
    db.add(lecture)
    db.commit()
    db.refresh(lecture)
    return lecture
