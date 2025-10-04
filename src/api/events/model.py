from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class SignupRequest(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    teacher: str
    CPA: float
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


class StudentModel(SQLModel, table=True):
    student_id: int = Field(index=True, primary_key=True) # /about, /contact, # pricing
    first_name: Optional[str] = Field(default="", index=True) # browser
    last_name: Optional[str] = Field(default="", index=True)
    teacher: Optional[str] = Field(default="", index=True) 
    CPA: Optional[float] = Field(index=True)
    email: str = Field(index=True, unique=True)
    password_hash: str

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"
