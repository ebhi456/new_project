from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse
)

router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"]
)


@router.get("/", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


@router.post("/", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Employee).filter(
        Employee.email == employee.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Employee already exists"
        )

    new_employee = Employee(
        employee_id=employee.employee_id,
        name=employee.name,
        email=employee.email,
        department=employee.department,
        designation=employee.designation
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee