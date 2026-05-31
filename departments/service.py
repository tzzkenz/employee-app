from datetime import UTC, datetime

from departments import repository
from employees import repository as employee_repository
from departments.schema import DepartmentCreate
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.handler import NotFoundException
from models.department import Department


async def create_department(body: DepartmentCreate, db: AsyncSession):

  department = Department()
  department.name = body.name.strip()

  return await repository.create_department(department, db)

async def get_all_departments(db: AsyncSession):
  return await repository.get_all_departments(db)

async def get_department(department_id: int, db: AsyncSession):
  department = await repository.get_department(department_id, db)
  if department is None:
    raise NotFoundException("Department not found")
  return department

async def patch_department(department_id: int, body: DepartmentCreate, db: AsyncSession):
  original_department = await repository.get_department(department_id, db)

  if original_department is None:
    raise NotFoundException("Department not found")

  if body.name is not None:
    original_department.name = body.name.strip()

  return await repository.patch_department(original_department, db)

async def delete_department(department_id: int,  db: AsyncSession):
  original_department = await repository.get_department(department_id, db)
  
  if original_department is None:
    raise NotFoundException("Department not found")
  
  original_department.deleted_at = datetime.now(UTC)
  return await repository.delete_department(original_department, db)
   
async def add_employee_to_department(department_id: int, employee_id: int, db: AsyncSession):
  department = await repository.get_department_with_employees(department_id, db)

  if department is None:
    raise NotFoundException("Department not found")

  employee = await employee_repository.get_employee(employee_id, db)

  if employee is None:
    raise NotFoundException("Employee not found")

  department.employees.append(employee)
  return await repository.add_employee_to_department(department, db)

async def get_all_employees_in_department(department_id: int, db: AsyncSession):
  return await repository.get_all_employees_in_department(department_id, db)

async def delete_employee_from_department(department_id: int, employee_id: int, db: AsyncSession):
  department = await repository.get_department_with_employees(department_id, db)

  if department is None:
    raise NotFoundException("Department not found")
  
  employee = await employee_repository.get_employee(employee_id, db)

  if employee is None:
    raise NotFoundException("Employee not found")
  
  department.employees.remove(employee)
  return await repository.delete_employee_from_department(department, db)