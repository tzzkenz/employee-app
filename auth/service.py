import email

from fastapi import HTTPException
from jose import JWTError, jwt

from auth.schema import LoginRequest
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import create_access_token, create_refresh_token, verify_password
from config import settings
from employees.repository import get_by_email
from exceptions.handler import UnauthorizedException


async def login(form: LoginRequest, db: AsyncSession):
  employee = await get_by_email(form.username, db)

  if employee is None:
    raise UnauthorizedException("Invalid email or password")
  if not verify_password(form.password, employee.password_hash):
    raise UnauthorizedException("Invalid email or password")

  access_token = create_access_token({"id" : employee.id, "email" : employee.email, "role": employee.role}) 
  refresh_token = create_refresh_token({"id" : employee.id, "email" : employee.email, "role": employee.role}) 

  return {
    "access_token" : access_token,
    "refresh_token" : refresh_token,
    "token_type" : "bearer"
  }



def refresh_token_service(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )

        if payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid refresh token")

        email = payload.get("email")
        id = payload.get("id")

        new_access_token = create_access_token({
            "id": id,
            "email": email
        })

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise UnauthorizedException("Invalid or expired refresh token")