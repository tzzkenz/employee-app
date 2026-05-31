from fastapi import APIRouter, Depends
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from auth import service
from auth.schema import LoginRequest, RefreshRequest, TokenResponse
from database.connection import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
  token = await service.login(body, db)
  return token

@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshRequest):
    return service.refresh_token_service(body.refresh_token)