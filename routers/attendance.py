from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session, select
from database.connection import get_session
from models.models import Attendance, Employee
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/attendance", tags=["attendance"])

class ClockPayload(BaseModel):
    lat: float | None = None
    lon: float | None = None

def get_current_employee(x_user_id: int = Header(...), session: Session = Depends(get_session)):
    emp = session.get(Employee, x_user_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.post("/clockin")
def clock_in(payload: ClockPayload, emp: Employee = Depends(get_current_employee), session: Session = Depends(get_session)):
    att = Attendance(employee_id=emp.id, clock_in=datetime.utcnow(), lat=payload.lat, lon=payload.lon)
    session.add(att)
    session.commit()
    session.refresh(att)
    return {"message": "clocked in", "attendance_id": att.id, "clock_in": att.clock_in}

@router.post("/clockout")
def clock_out(payload: ClockPayload, emp: Employee = Depends(get_current_employee), session: Session = Depends(get_session)):
    # find last attendance without clock_out
    q = select(Attendance).where(Attendance.employee_id == emp.id).order_by(Attendance.id.desc())
    last = session.exec(q).first()
    if not last or last.clock_out is not None:
        raise HTTPException(status_code=400, detail="No active clock-in found")
    last.clock_out = datetime.utcnow()
    if payload.lat is not None:
        last.lat = payload.lat
    if payload.lon is not None:
        last.lon = payload.lon
    session.add(last)
    session.commit()
    session.refresh(last)
    return {"message": "clocked out", "attendance_id": last.id, "clock_out": last.clock_out}
