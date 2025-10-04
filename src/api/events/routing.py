from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import case, func
from timescaledb.hyperfunctions import time_bucket
from api.db.db_session import get_session
from ..joblib.password import verify_password, hash_password


from .model import StudentModel, SignupRequest, LoginRequest

router = APIRouter()

router = APIRouter(prefix="/students", tags=["students"])


# 👉 POST: thêm student mới
# @router.post("/", response_model=StudentModel)
# def create_student(student: StudentModel, session: Session = Depends(get_session)):
#     session.add(student)
#     session.commit()
#     session.refresh(student)
#     return student

@router.post("/signup")
def signup(data: SignupRequest, session: Session = Depends(get_session)):
    # check email đã tồn tại chưa
    existing = session.exec(select(StudentModel).where(StudentModel.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    student = StudentModel(
        student_id=data.student_id,
        email=data.email,
        password_hash=hash_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        teacher=data.teacher,
        CPA=data.CPA
    )
    session.add(student)
    session.commit()
    session.refresh(student)
    return {"message": "Signup successful", "student_id": student.student_id}


@router.post("/login")
def login(data: LoginRequest, session: Session = Depends(get_session)):
    email = data.email
    password = data.password
    student = session.exec(select(StudentModel).where(StudentModel.email == email)).first()
    if not student or not verify_password(password, student.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful", "student_id": student.student_id}


# 👉 GET: lấy tất cả students
@router.get("/", response_model=List[StudentModel])
def get_students(session: Session = Depends(get_session)):
    students = session.exec(select(StudentModel)).all()
    return students


# 👉 GET: lấy student theo id
@router.get("/details/{student_id}", response_model=StudentModel)
def get_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(StudentModel, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# 👉 GET: học sinh siêu giỏi (CPA > 3.8)
@router.get("/super", response_model=List[StudentModel])
def get_super_students(session: Session = Depends(get_session)):
    statement = select(StudentModel).where(StudentModel.CPA > 3.8)
    results = session.exec(statement).all()
    return results
