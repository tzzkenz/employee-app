from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
import employees.service as service
from employees.schema import AddressCreate, AddressPatch, AddressResponse, EmployeeCreate, EmployeePatch, EmployeeResponse
from auth.dependencies import get_current_user
from auth.schema import TokenPayload

router = APIRouter(prefix="/employee", tags=["Employee"])

@router.post("", response_model=EmployeeResponse)
async def create_employee(body: EmployeeCreate, db: AsyncSession = Depends(get_db)):
  return await service.create_employee(body, db)

@router.get("", response_model=list[EmployeeResponse])
async def get_all_employees(db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user)):
  return await service.get_all_employees(db)

@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
  return await service.get_employee(employee_id, db)

@router.delete("/{employee_id}", response_model=EmployeeResponse)
async def delete_employee(employee_id: int, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user)):
  return await service.delete_employee(employee_id, db)

@router.patch("/{employee_id}", response_model=EmployeeResponse)
async def patch_employee(employee_id: int, body: EmployeePatch, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user)):
  return await service.patch_employee(employee_id, body, db)

@router.post("/{employee_id}/address", response_model=AddressResponse)
async def create_address(employee_id: int, body: AddressCreate, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user)):
  return await service.create_address(employee_id, body, db)

@router.get("/address/{address_id}", response_model=AddressResponse)
async def get_address(address_id: int, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user)):
  return await service.get_address(address_id, db)

@router.get("/{employee_id}/address", response_model=list[AddressResponse])
async def get_all_addresses(employee_id: int,  db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user)):
  return await service.get_all_addresses(employee_id, db)

@router.delete("{employee_id}/address/{address_id}", response_model=AddressResponse)
async def delete_address(employee_id: int, address_id: int, db: AsyncSession = Depends(get_db)):
  return await service.delete_address(employee_id, address_id, db)

@router.patch("/address/{address_id}", response_model=AddressResponse)
async def patch_address(address_id: int, body: AddressPatch, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user)):
  return await service.patch_address(address_id, body, db)

@router.post("/{employee_id}/department/{department_id}", response_model=EmployeeResponse)
async def add_department_to_employee(employee_id: int, department_id: int, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user)):
    return await service.add_department_to_employee(employee_id, department_id, db)

@router.delete("/{employee_id}/department/{department_id}", response_model=EmployeeResponse)
async def delete_department_from_employee(employee_id: int, department_id: int, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user)):
   return await service.delete_department_from_employee(employee_id, department_id, db)