from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import User, Course, Lecture, StudentLectureStats
from app.database import SessionLocal, engine
from app.utils import create_user, register_course, create_lecture

# Initialize FastAPI app
app = FastAPI()

# Database setup
# Create tables (if not already created)
from app.models import Base
Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class CourseCreate(BaseModel):
    name: str
    description: str
    tutor_id: int

class LectureCreate(BaseModel):
    course_id: int
    start_time: str
    end_time: str

@app.post("/create_user")
async def create_user_endpoint(user: UserCreate):
    db = SessionLocal()
    try:
        user_obj = create_user(db, user.username, user.email, user.password)
        return {"message": "User created successfully", "user_id": user_obj.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.post("/register_course")
async def register_course_endpoint(course: CourseCreate):
    db = SessionLocal()
    try:
        course_obj = register_course(db, course.name, course.description, course.tutor_id)
        return {"message": "Course registered successfully", "course_id": course_obj.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.post("/create_lecture")
async def create_lecture_endpoint(lecture: LectureCreate):
    db = SessionLocal()
    try:
        lecture_obj = create_lecture(db, lecture.course_id, lecture.start_time, lecture.end_time)
        return {"message": "Lecture created successfully", "lecture_id": lecture_obj.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
