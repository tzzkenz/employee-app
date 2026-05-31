from auth.schema import LoginRequest
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import create_access_token, verify_password
from employees.repository import get_by_email
from exceptions.handler import UnauthorizedException


async def login(body: LoginRequest, db: AsyncSession):
  employee = await get_by_email(body.email, db)

  if employee is None:
    raise UnauthorizedException("Invalid email or password")
  if not verify_password(body.password, employee.password_hash):
    raise UnauthorizedException("Invalid email or password")

  return create_access_token({"id" : employee.id, "email" : employee.email}) 
