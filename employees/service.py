from sqlalchemy.ext.asyncio import AsyncSession

import employees.repository as repository
import departments.repository as department_repository
from employees.schema import AddressCreate, AddressPatch, EmployeeCreate, EmployeePatch
from exceptions.handler import NotFoundException
from models import address
from models.address import Address
from models.employee import Employee


async def create_employee( body: EmployeeCreate, db: AsyncSession) -> Employee:
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
  employees = await repository.get_all_employees(db)

  return employees

async def get_employee( employee_id: int, db: AsyncSession) -> Employee:
  employee = await repository.get_employee(employee_id, db)
  if employee is None or employee.deleted_at is not None:
    raise NotFoundException(detail="Employee not found in DB")

  return employee

async def delete_employee(employee_id: int, db: AsyncSession)  -> Employee:
  employee: Employee = await repository.get_employee(employee_id, db)

  if employee is None or employee.deleted_at is not None:
    raise NotFoundException(detail="Employee not found in DB")
  
  deleted_employee: Employee = await repository.delete_employee(employee,db)

  return deleted_employee

async def patch_employee(employee_id: int, body: EmployeePatch, db: AsyncSession, ) -> Employee:
  original_employee: Employee = await repository.get_employee(employee_id, db)

  if original_employee is None or original_employee.deleted_at is not None:
    raise NotFoundException("Requested employee is not present in the DB")

  if body.name is not None:
    original_employee.name = body.name.strip()
  if body.email is not None:
    original_employee.email = body.email.strip()
  if body.age is not None:
    original_employee.age = body.age

  patched_employee = await repository.patch_employee(db, original_employee)
  return patched_employee
  

async def create_address(employee_id: int, body: AddressCreate, db: AsyncSession) -> Address:
  employee = await repository.get_employee(employee_id, db)

  if employee is None or employee.deleted_at is not None:
    raise NotFoundException("Requested employee is not present in the DB")
  
  address = Address()
  address.street = body.street.strip()
  address.city = body.city.strip()
  address.country = body.country.strip()
  address.postal_code = body.postal_code.strip()

  return await repository.create_address(employee, address, db)

async def get_address(address_id: int, db: AsyncSession) -> Address:
  address: Address = await repository.get_address(address_id, db)
  
  if address is None or address.deleted_at is not None:
    raise NotFoundException(detail="The given address was not found in the DB")
  
  return address

async def delete_address(address_id: int, db: AsyncSession) -> Address:
  address: Address = await repository.get_address(address_id, db)

  if address is None or address.deleted_at is not None:
    raise NotFoundException(detail="The given address was not found in the DB")
  
  deleted_address: Address = await repository.delete_address(address, db)

  return deleted_address
  
async def patch_address(address_id: int, body: AddressPatch, db: AsyncSession) -> Address:
  original_address = await repository.get_address(address_id, db)

  if original_address is None or original_address.deleted_at is not None:
    raise NotFoundException(detail="The given address was not found in the DB")
  
  if body.street is not None:
    original_address.street = body.street.strip()
  if body.city is not None:
    original_address.city = body.city.strip()
  if body.country is not None:
    original_address.country = body.country.strip()
  if body.postal_code is not None:
    original_address.postal_code = body.postal_code.strip()

  patched_address = await repository.patch_address(original_address, db)
  return patched_address

async def get_all_addresses(employee_id: int, db: AsyncSession) -> list[Address]:
  addresses = await repository.get_all_addresses(employee_id, db)
  return addresses


async def add_department_to_employee( employee_id: int, department_id: int, db: AsyncSession) -> Employee:
  employee = await repository.get_employee_with_department(employee_id, db)
  department = await department_repository.get_department(department_id, db)

  if employee is None or employee.deleted_at is not None:
    raise NotFoundException("Employee not found")
  if department is None or department.deleted_at is not None:
    raise NotFoundException("Department not found")

  employee.departments.append(department)
  return await repository.add_department_to_employee(employee, db)

async def delete_department_from_employee(employee_id: int, department_id: int, db: AsyncSession) -> Employee:
  employee = await repository.get_employee_with_department(employee_id, db)
  department = await department_repository.get_department(department_id, db)

  if employee is None or employee.deleted_at is not None:
    raise NotFoundException("Employee not found")
  if department is None or department.deleted_at is not None:
    raise NotFoundException("Department not found")
  
  employee.departments.remove(department)
  return await repository.delete_department_from_employee(employee, db)