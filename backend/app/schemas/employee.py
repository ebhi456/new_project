from pydantic import BaseModel, EmailStr


class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    department: str
    designation: str


class EmployeeResponse(EmployeeCreate):
    id: int

    class Config:
        from_attributes = True