from typing import List
from sqlalchemy.orm import Session
import app.models as models
import app.Schema as schema
import uuid
from app.db import get_db
from fastapi import APIRouter, HTTPException, status, Depends

router = APIRouter(prefix="/office", tags=["office"])

@router.get("/", response_model=List[schema.OfficeResponse])
def get_offices(db: Session = Depends(get_db)):
    """Return all offices"""
    offices = db.query(models.Office).all()
    return offices

@router.get("/{office_id}", status_code=status.HTTP_200_OK, response_model=schema.OfficeResponse)
def get_office(office_id: int, db: Session = Depends(get_db)):
    """Return office details"""
    office = db.query(models.Office).filter(models.Office.id == office_id).first()
    if office is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Office not found")

    return office

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[schema.OfficeResponse])
def create_office(office: schema.CreateOffice, db: Session = Depends(get_db)):
    """Create a new office"""
    new_office = models.Office(**office.model_dump())
    db.add(new_office)
    db.commit()
    db.refresh(new_office)

    return [new_office]

@router.delete("/{office_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_office(office_id: int, db: Session = Depends(get_db)):
    """Delete an office"""
    deleted_office = db.query(models.Office).filter(models.Office.id == office_id)
    if deleted_office is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Office not found")
    deleted_office.delete(synchronize_session=False)
    db.commit()

@router.patch("/{office_id}", response_model=schema.OfficeResponse)
def patch_office(update_data: schema.UpdateOffice, office_id: int, db: Session = Depends(get_db)):
    """Patch an office"""
    office_query = db.query(models.Office).filter(models.Office.id == office_id)
    office = office_query.first()

    if office is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Office not found")

    update_dict = update_data.model_dump(exclude_unset=True)

    if update_dict:
        office_query.update(update_dict, synchronize_session=False)
        db.commit()
        db.refresh(office)

    return office