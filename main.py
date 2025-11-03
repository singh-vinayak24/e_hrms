from fastapi import FastAPI
from database.connection import init_db
from routers import auth, employees, attendance, leave, payroll, appraisal, recruitment

app = FastAPI(title="E-HRMS (MVP)", version="0.1")

# include routers
app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(leave.router)
app.include_router(payroll.router)
app.include_router(appraisal.router)
app.include_router(recruitment.router)

@app.on_event("startup")
def on_startup():
    init_db()
