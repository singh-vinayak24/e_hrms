from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database.connection import get_session
from models.models import Appraisal
from typing import List

router = APIRouter(prefix="/appraisal", tags=["appraisal"])

@router.get("/{employee_id}", response_model=List[Appraisal])
def get_appraisals(employee_id: int, session: Session = Depends(get_session)):
    q = select(Appraisal).where(Appraisal.employee_id == employee_id)
    return session.exec(q).all()
