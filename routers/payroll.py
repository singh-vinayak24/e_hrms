from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database.connection import get_session
from models.models import Employee, Payroll
from datetime import datetime

router = APIRouter(prefix="/payroll", tags=["payroll"])

@router.post("/generate/{employee_id}")
def generate_payroll(employee_id: int, session: Session = Depends(get_session)):
    emp = session.get(Employee, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
 
    tax = emp.salary * 0.10
    net = emp.salary - tax
    payroll = Payroll(employee_id=employee_id, amount=net, generated_at=datetime.utcnow())
    session.add(payroll)
    session.commit()
    session.refresh(payroll)
    return {"employee_id": employee_id, "gross_salary": emp.salary, "tax": tax, "net": net, "payroll_id": payroll.id}
