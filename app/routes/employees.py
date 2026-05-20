from typing import List
from sqlalchemy.orm import Session
from starlette import status
import app.models as models
import app.Schema as schema
import uuid
from app.Schema import CreateEmployee
from app.db import get_db
from fastapi import APIRouter, HTTPException, status, Depends

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("/", response_model=List[schema.EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    """Retrieve all employees"""
    employees = db.query(models.Employee).all()
    return employees

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema.EmployeeResponse)
def get_employee(id: uuid.UUID, db: Session = Depends(get_db)):
    """Retrieve an employee"""
    idv_employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    if idv_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return idv_employee

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[schema.EmployeeResponse])
def create_employee(employee: schema.CreateEmployee, db: Session = Depends(get_db)):
    """Create a new employee"""
    new_employee = models.Employee(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return [new_employee]

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: uuid.UUID, db: Session = Depends(get_db)):
    """Delete an employee"""
    deleted_employee = db.query(models.Employee).filter(models.Employee.id == id)
    if deleted_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    deleted_employee.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}", response_model=schema.EmployeeResponse)
def update_employee(update_employee: schema.EmployeeBase, id: uuid.UUID, db: Session = Depends(get_db)):
    """Update everything about an employee"""
    updated_employee = db.query(models.Employee).filter(models.Employee.id == id)
    employee = updated_employee.first()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    updated_employee.update(update_employee.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(employee)

    return employee

@router.patch("/{id}", response_model=schema.EmployeeResponse)
def patch_employee(update_data: schema.UpdateEmployee, id: uuid.UUID, db: Session = Depends(get_db)):
    """Patch an employee"""
    employee_query = db.query(models.Employee).filter(models.Employee.id == id)
    employee = employee_query.first()

    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    update_dict = update_data.model_dump(exclude_unset=True)

    if update_dict:
        employee_query.update(update_dict, synchronize_session=False)
        db.commit()
        db.refresh(employee)

    return employee