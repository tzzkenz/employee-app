from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from exceptions.handler import AppException, ConflictException
from models.department import Department
from sqlalchemy.ext.asyncio import AsyncSession

from models.employee import Employee

async def create_department(department: Department, db: AsyncSession):
  db.add(department)

  try:
    await db.commit()
  except:
    await db.rollback()
    raise ConflictException(detail=f"Email '{department}' is already in use")
  
  await db.refresh(department)
  return department

async def get_all_departments(db: AsyncSession):
  statement = select(Department).where(Department.deleted_at.is_(None))
  result = await db.scalars(statement)
  return result.all()

async def get_department(department_id: int, db: AsyncSession):
  statement = select(Department).where(Department.deleted_at.is_(None), Department.id == department_id)
  result = await db.scalars(statement)
  return result.one()

async def patch_department(original_department: Department, db: AsyncSession):
  try:
    await db.commit()
  except IntegrityError as e:
    await db.rollback()
    raise AppException(detail=f"Something went wrong: {str(e)}")
    
  await db.refresh(original_department)

  return original_department

async def delete_department(original_department: Department, db: AsyncSession):
  try:
    await db.commit()
  except IntegrityError as e:
    await db.rollback()
    raise AppException(detail=f"Something went wrong: {str(e)}")
    
  await db.refresh(original_department)

  return original_department

async def get_department_with_employees(department_id: id, db: AsyncSession):
  statement = select(Department).options(selectinload(Department.employees)).where(Department.id == department_id)
  result = await db.scalars(statement)
  return result.first()

async def add_employee_to_department(department: Department, db: AsyncSession):
  try:
    await db.commit()
  except IntegrityError as e:
    await db.rollback()
    raise AppException(detail=f"Something went wrong: {str(e)}")
    
  await db.refresh(department)
  return department

async def get_all_employees_in_department(department_id: int, db: AsyncSession):
  statement = select(Employee).join(Employee.departments).where(Department.id == department_id)
  result = await db.scalars(statement)
  return result.all()

async def delete_employee_from_department(department: Department, db: AsyncSession):
  try:
    await db.commit()
  except IntegrityError as e:
    await db.rollback()
    raise AppException(detail=f"Something went wrong: {str(e)}")
    
  await db.refresh(department)
  return department