from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from exceptions.handler import AppException
from models.department import Department
from sqlalchemy.ext.asyncio import AsyncSession

from models.employee import Employee

async def save(entity, db: AsyncSession):
  try:
    await db.commit()
  except IntegrityError as e:
    await db.rollback()
    raise AppException(detail=f"Something went wrong: {str(e)}")
  await db.refresh(entity)
  return entity

async def create_department(department: Department, db: AsyncSession) -> Department:
  db.add(department)
  return await save(department, db)

async def get_all_departments(db: AsyncSession) -> list[Department]:
  statement = select(Department).where(Department.deleted_at.is_(None))
  result = await db.scalars(statement)
  return result.all()
 
async def get_department(department_id: int, db: AsyncSession) -> Department:
  statement = select(Department).where( Department.id == department_id, Department.deleted_at.is_(None))
  result = await db.scalars(statement)
  return result.one_or_none()

async def patch_department(original_department: Department, db: AsyncSession) -> Department:
  return await save(original_department, db)

async def delete_department(original_department: Department, db: AsyncSession) -> Department:
  return await save(original_department, db)

async def get_department_with_employees(department_id: int, db: AsyncSession) -> Department:
  statement = select(Department).options(selectinload(Department.employees)).where(Department.id == department_id, Department.deleted_at.is_(None))
  result = await db.scalars(statement)
  return result.one_or_none()

async def add_employee_to_department(department: Department, db: AsyncSession):
  return await save(department, db)

async def get_all_employees_in_department(department_id: int, db: AsyncSession) -> list[Employee]:
  statement = select(Employee).join(Employee.departments).where(Department.id == department_id, Department.deleted_at.is_(None))
  result = await db.scalars(statement)
  return result.all()

async def delete_employee_from_department(department: Department, db: AsyncSession) -> Department:
  return await save(department, db)