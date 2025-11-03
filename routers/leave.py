from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session
from database.connection import get_session
from models.models import LeaveRequest, Employee
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/leave", tags=["leave"])

class LeaveRequestIn(BaseModel):
    start_date: datetime
    end_date: datetime
    reason: str | None = None

def get_current_employee(x_user_id: int = Header(...), session: Session = Depends(get_session)):
    emp = session.get(Employee, x_user_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.post("/request")
def request_leave(payload: LeaveRequestIn, emp: Employee = Depends(get_current_employee), session: Session = Depends(get_session)):
    lr = LeaveRequest(employee_id=emp.id, start_date=payload.start_date, end_date=payload.end_date, reason=payload.reason)
    session.add(lr)
    session.commit()
    session.refresh(lr)
    return {"message": "leave requested", "leave_id": lr.id}

@router.post("/approve/{leave_id}")
def approve_leave(leave_id: int, approve: bool, session: Session = Depends(get_session)):
    lr = session.get(LeaveRequest, leave_id)
    if not lr:
        raise HTTPException(status_code=404, detail="Leave not found")
    lr.status = "approved" if approve else "rejected"
    session.add(lr)
    session.commit()
    return {"message": f"leave {lr.status}"}
