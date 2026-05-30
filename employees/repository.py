from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.handler import AppException, ConflictException
from models import Employee
from models.address import Address

async def create_employee( employee: Employee, db: AsyncSession) -> Employee:
  db.add(employee)

  try:
    await db.commit()
  except:
    await db.rollback()
    raise ConflictException(detail=f"Email '{employee.email}' is already in use")
  
  await db.refresh(employee)
  return employee

async def get_all(db: AsyncSession) -> list[Employee]:
  statement = select(Employee).where(Employee.deleted_at.is_(None))
  result = await db.scalars(statement)

  return result.all()

async def get_employee(id: int, db: AsyncSession ) -> Employee:
  statement = select(Employee).where(Employee.deleted_at.is_(None), Employee.id == id)
  result = await db.scalars(statement)

  return result.one()

async def delete_employee(db: AsyncSession, employee: Employee) -> Employee:
  employee.deleted_at = datetime.now()
  db.add(employee)
  
  try:
    db.commit()
  except IntegrityError as e:
    db.rollback()
    raise AppException(detail=f"Something went wrong: {str(e)}")
  
  await db.refresh(employee)
  return employee

async def patch_employee(db: AsyncSession, original_employee: Employee) -> Employee:
  try:
      await db.commit()
  except IntegrityError as e:
      await db.rollback()
      raise AppException(detail=f"Something went wrong: {str(e)}")
    
  await db.refresh(original_employee)

  return original_employee


async def create_address(employee: Employee, address: Address, db: AsyncSession):

  address.employee = employee
  db.add(address)

  try:
    await db.commit()
  except IntegrityError as e:
    await db.rollback()
    raise AppException(detail=f"Something went wrong: {str(e)}")
    
  await db.refresh(address)
  return address

async def get_address(address_id: int, db: AsyncSession):
  statement = select(Address).where(Address.deleted_at.is_(None), Address.id == address_id)
  address = await db.scalars(statement)
  return address.first()

async def delete_address(deleted_address: Address, db: AsyncSession):
  deleted_address.deleted_at = datetime.now()
  db.add(deleted_address)

  try:
    await db.commit()
  except IntegrityError as e:
    await db.rollback()
    raise AppException(detail=f"Something went wrong: {str(e)}")
  
  await db.refresh(deleted_address)
  return deleted_address

async def patch_address(original_address: Address, db: AsyncSession):
  try:
      await db.commit()
  except IntegrityError as e:
      await db.rollback()
      raise AppException(detail=f"Something went wrong: {str(e)}")
    
  await db.refresh(original_address)

  return original_address

async def get_all_addresses(id: int, db: AsyncSession):
  statement = select(Address).where(Address.deleted_at.is_(None), Address.employee_id == id)
  result = await db.scalars(statement)

  return result.all()