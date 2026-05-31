from sqlalchemy.ext.asyncio import AsyncSession

import employees.repository as repository
import departments.repository as department_repository
from employees.schema import AddressCreate, EmployeeCreate, EmployeePatch
from exceptions.handler import BadRequestException, NotFoundException
from models import employee
from models.address import Address
from models.employee import Employee


async def create_employee( body: EmployeeCreate, db: AsyncSession):
  employee: Employee = Employee()

  employee.name = body.name.strip()
  employee.age = body.age
  employee.email = body.email.strip()

  if body.address:
    address = Address()
    address.street = body.address.street.strip()
    address.city = body.address.city.strip()
    address.country = body.address.country.strip()
    address.postal_code = body.address.postal_code.strip()

    employee.addresses.append(address)
  
  employee = await repository.create_employee(employee, db)
  return employee

async def get_all_employees(db: AsyncSession) -> list[Employee]:
  employees = await repository.get_all(db)

  return employees

async def get_employee( id: int, db: AsyncSession) -> Employee:
  employee = await repository.get_employee(id, db)

  if employee is None:
    raise NotFoundException(detail="Employee not found in DB")

  return employee

async def delete_employee(id: int, db: AsyncSession)  -> Employee:
  employee: Employee = await repository.get_employee(id, db)

  if employee is None or employee.deleted_at is not None:
    raise NotFoundException(detail="Employee not found in DB")
  
  deleted_employee: Employee = await repository.delete_employee(db, employee)

  return deleted_employee

async def patch_employee(id: int, body: EmployeePatch, db: AsyncSession, ) -> Employee:
  original_employee: Employee = await repository.get_employee(id, db)

  if original_employee is None:
    raise NotFoundException("Requested employee is not present in the DB")

  if body.name is not None:
    original_employee.name = body.name
  if body.email is not None:
    original_employee.email = body.email
  if body.age is not None:
    original_employee.age = body.age
  # if body.address is not None:
  #   address = Address()
  #   if body.address.street is not None:
  #     address.street = body.address.street  
  #   if body.address.city is not None:
  #     address.city = body.address.city  
  #   if body.address.country is not None:
  #     address.country = body.address.country  
  #   if body.address.postal_code is not None:
  #     address.postal_code = body.address.postal_code

    # original_employee.addresses.append(address)  

  patched_employee = await repository.patch_employee(db, original_employee)
  return patched_employee
  

async def create_address(id: int, body: AddressCreate, db: AsyncSession):
  employee = await repository.get_employee(id, db)

  if employee is None or employee.deleted_at is not None:
    raise NotFoundException("Requested employee is not present in the DB")
  
  address = Address()
  address.street = body.street.strip()
  address.city = body.city.strip()
  address.country = body.country.strip()
  address.postal_code = body.postal_code.strip()

  return await repository.create_address(employee, address, db)

async def get_address(address_id: int, db: AsyncSession):
  address: Address = await repository.get_address(address_id, db)
  
  if address is None:
    raise NotFoundException(detail="The given address was not found in the DB")
  
  return address

async def delete_address(address_id: int, db: AsyncSession):
  address: Address = await repository.get_address(address_id, db)

  if address is None:
    raise NotFoundException(detail="The given address was not found in the DB")
  
  deleted_address: Address = await repository.delete_address(address, db)

  return deleted_address
  
async def patch_address(address_id: int, body: EmployeePatch, db: AsyncSession):
  original_address = await repository.get_address(address_id, db)

  if original_address is None:
    raise NotFoundException(detail="The given address was not found in the DB")
  
  if body.street is not None:
    original_address.street = body.street
  if body.city is not None:
    original_address.city = body.city
  if body.country is not None:
    original_address.country = body.country
  if body.postal_code is not None:
    original_address.postal_code = body.postal_code

  patched_address = await repository.patch_address(original_address, db)
  return patched_address

async def get_all_addresses(id: int, db: AsyncSession):
  employees = await repository.get_all_addresses(id, db)
  return employees


async def add_department_to_employee( employee_id: int, department_id: int, db: AsyncSession):
  employee = await repository.get_employee_with_department(employee_id, db)
  department = await department_repository.get_department(department_id, db)

  employee.departments.append(department)
  return await repository.add_department_to_employee(employee, db)

async def delete_department_from_employee(employee_id: id, department_id: int, db: AsyncSession):
  employee = await repository.get_employee_with_department(employee_id, db)
  department = await department_repository.get_department(department_id, db)
  
  employee.departments.remove(department)
  return await repository.delete_department_from_employee(employee, db)