import uuid

from sqlalchemy.orm import relationship

from app.db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey


class Office(Base):
    __tablename__ = "office"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    number = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    employee = relationship("Employee", back_populates="office")

class Employee(Base):
    __tablename__ = "employee"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    salary = Column(String, nullable=True)
    office_id = Column(Integer, ForeignKey("office.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    office = relationship("Office", back_populates="employee")

