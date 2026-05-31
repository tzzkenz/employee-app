from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRequest(BaseModel):
  model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

  email: EmailStr
  password: str

class TokenResponse(BaseModel):
  model_config = ConfigDict(
    from_attributes=True
  )

  access_token: str

class TokenPayload(BaseModel):
  id: int
  email: EmailStr
