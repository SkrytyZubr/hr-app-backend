import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# ========== Office schemas ==========
class OfficeBase(BaseModel):
    country: str
    city: str
    street: str
    number: str
    phone: str

    model_config = {
        "from_attributes": True
    }

class OfficeResponse(BaseModel):
    id: int
    country: str
    city: str
    street: str
    number: str
    phone: str

class CreateOffice(OfficeBase):
    model_config = {
        "from_attributes": True
    }

class UpdateOffice(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    number: Optional[str] = None
    phone: Optional[str] = None

# ========== Employee schemas ==========
class EmployeeBase(BaseModel):
    name: str
    surname: str
    email: str
    office_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

class EmployeeResponse(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    email: str
    office: Optional[OfficeResponse] = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class CreateEmployee(EmployeeBase):
    model_config = {
        "from_attributes": True
    }

class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    office_id: Optional[int] = None