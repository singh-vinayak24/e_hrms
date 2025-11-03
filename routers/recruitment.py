from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session
from database.connection import get_session
from models.models import Candidate

router = APIRouter(prefix="/candidates", tags=["recruitment"])

@router.post("/")
def create_candidate(name: str, email: str | None = None, resume: UploadFile | None = File(None), session: Session = Depends(get_session)):
    resume_path = None
    if resume:
        path = f"uploads/resume_{resume.filename}"
        with open(path, "wb") as f:
            f.write(resume.file.read())
        resume_path = path
    cand = Candidate(name=name, email=email, resume_path=resume_path)
    session.add(cand)
    session.commit()
    session.refresh(cand)
    return {"id": cand.id, "name": cand.name, "status": cand.status}
