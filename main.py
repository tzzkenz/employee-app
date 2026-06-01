from contextlib import asynccontextmanager

from fastapi import FastAPI
from uvicorn import lifespan
from database import create_tables
from exceptions.handler import register_exception_handlers
from middleware import RequestLoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from employees.router import router as employee_router
from auth.router import router as auth_router
from departments.router import router as department_router
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
  await create_tables()
  yield

app = FastAPI(
  title="Employee CRUD API",
  description="Documentation for CRUD API of a simple employee app",
  version="1.0.0",
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=False,
  allow_methods=["*"],
  allow_headers=["*"],
  expose_headers=["*"]
)

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s %(levelname)s %(name)s %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
)

app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(department_router)

register_exception_handlers(app)

@app.get("/health", tags=["Health Check"])
def health():
  return {"message" : f"App is healthy"}