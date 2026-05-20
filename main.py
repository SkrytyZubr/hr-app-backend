from fastapi import FastAPI
from app import db
import psycopg2
from app.db import engine
from app.routes.employees import router as employees_router
from app.routes.office import router as office_router

app = FastAPI()

app.include_router(employees_router)
app.include_router(office_router)