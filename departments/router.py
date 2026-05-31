from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from departments import service
from departments.schema import DepartmentCreate, DepartmentResponse
from employees.schema import EmployeeResponse

router = APIRouter(prefix="/department", tags=["Department"])

@router.post("", response_model=DepartmentResponse)
async def create_department(body: DepartmentCreate, db:AsyncSession = Depends(get_db)):
  return await service.create_department(body, db)

@router.get("", response_model=list[DepartmentResponse])
async def get_all_departments(db:AsyncSession = Depends(get_db)):
  return await service.get_all_departments(db)

@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(department_id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_department(department_id, db)

@router.patch("/{department_id}", response_model=DepartmentResponse)
async def patch_department(department_id: int, body: DepartmentCreate, db: AsyncSession = Depends(get_db)):
  return await service.patch_department(department_id, body, db)
  
@router.delete("/{department_id}", response_model=DepartmentResponse)
async def delete_department(department_id: int, db: AsyncSession = Depends(get_db)):
  return await service.delete_department(department_id, db)

@router.post("/{department_id}/employee/{employee_id}", response_model=EmployeeResponse)
async def add_employee_to_department(department_id: int, employee_id: int, db: AsyncSession = Depends(get_db)):
    return await service.add_employee_to_department(department_id, employee_id, db)

@router.get("/{department_id}/employee", response_model=list[EmployeeResponse])
async def get_all_employees_in_department(department_id: int, db: AsyncSession = Depends(get_db)):
    return await service.get_all_employees_in_department(department_id, db)

@router.delete("/{department_id}/employee/{employee_d}", response_model=EmployeeResponse)
async def delete_employee_from_department(department_id: int, employee_id: int, db: AsyncSession = Depends(get_db)):
   return await service.delete_employee_from_department(department_id, employee_id, db)
