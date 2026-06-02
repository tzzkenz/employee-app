from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependencies import get_current_user
from auth.schema import TokenPayload
from database.connection import get_db
from departments import service
from departments.schema import DepartmentCreate, DepartmentPatch, DepartmentResponse
from employees.schema import EmployeeResponse

router = APIRouter(prefix="/department", tags=["Department"])


@router.post("", response_model=DepartmentResponse)
async def create_department(
    body: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    return await service.create_department(body, db)


@router.get("", response_model=list[DepartmentResponse])
async def get_all_departments(
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    return await service.get_all_departments(db)


@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    return await service.get_department(department_id, db)


@router.patch("/{department_id}", response_model=DepartmentResponse)
async def patch_department(
    department_id: int,
    body: DepartmentPatch,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    return await service.patch_department(department_id, body, db)


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    await service.delete_department(department_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{department_id}/employee/{employee_id}", response_model=EmployeeResponse)
async def add_employee_to_department(
    department_id: int,
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    return await service.add_employee_to_department(department_id, employee_id, db)


@router.get("/{department_id}/employee", response_model=list[EmployeeResponse])
async def get_all_employees_in_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    return await service.get_all_employees_in_department(department_id, db)


@router.delete(
    "/{department_id}/employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_employee_from_department(
    department_id: int,
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    await service.delete_employee_from_department(department_id, employee_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
