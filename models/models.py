from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: Optional[str] = None
    hashed_password: str
    role: str = "employee"  # admin | hr | employee

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    onboarded: bool = False
    salary: float = 0.0

class Attendance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

class LeaveRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int
    start_date: datetime
    end_date: datetime
    reason: Optional[str] = None
    status: str = "pending"  # pending | approved | rejected

class Payroll(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int
    amount: float
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: Optional[str] = None
    resume_path: Optional[str] = None
    status: str = "applied"

class Appraisal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int
    period: str  # e.g. '2025-Q1'
    score: float
    notes: Optional[str] = None
