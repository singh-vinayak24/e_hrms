from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database.connection import get_session
from models.models import Employee
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/employees", tags=["employees"])

class EmployeeCreate(BaseModel):
    name: str
    email: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = 0.0

class EmployeeUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    role: Optional[str]
    department: Optional[str]
    salary: Optional[float]

@router.post("/", response_model=Employee)
def create_employee(payload: EmployeeCreate, session: Session = Depends(get_session)):
    emp = Employee(**payload.dict(), onboarded=True)
    session.add(emp)
    session.commit()
    session.refresh(emp)
    return emp

@router.get("/", response_model=List[Employee])
def list_employees(session: Session = Depends(get_session)):
    return session.exec(select(Employee)).all()

@router.get("/{employee_id}", response_model=Employee)
def get_employee(employee_id: int, session: Session = Depends(get_session)):
    emp = session.get(Employee, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.put("/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, payload: EmployeeUpdate, session: Session = Depends(get_session)):
    emp = session.get(Employee, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    emp_data = payload.dict(exclude_unset=True)
    for k, v in emp_data.items():
        setattr(emp, k, v)
    session.add(emp)
    session.commit()
    session.refresh(emp)
    return emp

@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int, session: Session = Depends(get_session)):
    emp = session.get(Employee, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    session.delete(emp)
    session.commit()
    return None
