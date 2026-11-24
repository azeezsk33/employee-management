
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Employee Management System")

# Temporary storage
employees = []

class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float
    email: str

@app.get("/")
def home():
    return {"message": "Employee Management API"}

# Add employee
@app.post("/employees/")
def add_employee(emp: Employee):
    for employee in employees:
        if employee["id"] == emp.id:
            raise HTTPException(400, "Employee ID already exists")

    employees.append(emp.model_dump())
    return {"message": "Employee added successfully"}

# View employees
@app.get("/employees/")
def get_employees():
    return employees

# Search employee
@app.get("/employees/{emp_id}")
def get_employee(emp_id: int):
    for emp in employees:
        if emp["id"] == emp_id:
            return emp
    raise HTTPException(404, "Employee not found")

# Update employee
@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, updated: Employee):
    for i, emp in enumerate(employees):
        if emp["id"] == emp_id:
            if updated.id != emp_id:
                raise HTTPException(400, "Employee ID cannot be changed")
            employees[i] = updated.model_dump()
            return {"message": "Employee updated successfully"}

    raise HTTPException(404, "Employee not found")

# Delete employee
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    for emp in employees:
        if emp["id"] == emp_id:
            employees.remove(emp)
            return {"message": "Employee deleted successfully"}

    raise HTTPException(404, "Employee not found")
