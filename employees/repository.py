from datetime import UTC, datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from exceptions.handler import AppException
from models import Employee
from models.address import Address
  
  
async def save(entity, db: AsyncSession):
  try:
    await db.commit()
  except IntegrityError as e:
    await db.rollback()
    raise AppException(detail=f"Something went wrong: {str(e)}")
  await db.refresh(entity)
  return entity


async def create_employee( employee: Employee, db: AsyncSession) -> Employee:
  db.add(employee)
  return await save(employee, db)

async def get_all_employees(db: AsyncSession) -> list[Employee]:
  statement = select(Employee).where(Employee.deleted_at.is_(None))
  result = await db.scalars(statement)
  return result.all()

async def get_employee(employee_id: int, db: AsyncSession ) -> Employee | None:
  statement = select(Employee).where(Employee.deleted_at.is_(None), Employee.id == employee_id)
  result = await db.scalars(statement)
  return result.one_or_none()

async def delete_employee(employee: Employee, db: AsyncSession) -> Employee:
  employee.deleted_at = datetime.now(UTC)
  db.add(employee)
  return await save(employee, db)

async def patch_employee(db: AsyncSession, original_employee: Employee) -> Employee:
  return await save(original_employee, db)


async def create_address(employee: Employee, address: Address, db: AsyncSession) -> Address:
  address.employee = employee
  db.add(address)
  return await save(address, db)

async def get_address(address_id: int, db: AsyncSession) -> Address | None:
  statement = select(Address).where(Address.deleted_at.is_(None), Address.id == address_id)
  address = await db.scalars(statement)
  return address.one_or_none()

async def delete_address(deleted_address: Address, db: AsyncSession) -> Address:
  deleted_address.deleted_at = datetime.now(UTC)
  db.add(deleted_address)
  return await save(deleted_address, db)

async def patch_address(original_address: Address, db: AsyncSession) -> Address:
  return await save(original_address, db)

async def get_all_addresses(employee_id: int, db: AsyncSession) -> list[Address]:
  statement = select(Address).where(Address.deleted_at.is_(None), Address.employee_id == employee_id)
  result = await db.scalars(statement)
  return result.all()

async def get_employee_with_department(employee_id: int, db: AsyncSession) -> Employee | None:
  statement = select(Employee).options(selectinload(Employee.departments)).where(Employee.id == employee_id, Employee.deleted_at.is_(None))
  result = await db.scalars(statement)
  return result.one_or_none()

async def add_department_to_employee(employee: Employee, db: AsyncSession) -> Employee:
  return await save(employee, db)

async def delete_department_from_employee(employee: Employee, db: AsyncSession) -> Employee:
  return await save(employee, db)

async def get_by_email(email: str, db: AsyncSession) -> Employee:
  statement = select(Employee).where(Employee.email == email, Employee.deleted_at.is_(None))
  result = await db.scalars(statement)
  return result.one_or_none()