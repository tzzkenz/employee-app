from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

class AddressCreate(BaseModel):
  street: str = Field(min_length=3)
  city: str = Field(min_length=3)
  country: str = Field(min_length=3)
  postal_code: str = Field(min_length=3)

  @field_validator('postal_code')
  @classmethod
  def validate_postal_code(cls, value: str) -> str:
    if not value.isdigit():
      raise ValueError("postal_code value should be a digit (0-9)")    
    return value
    
  # @model_validator(mode='after')
  # def postal_code_length_for_country(self):
  #   pincodes = {
  #     "US": 5,
  #     "IN": 6
  #   }

  #   pincode = pincodes.get(self.country, None)
  #   if pincode is None:
  #     raise ValueError("Not a valid country")
        
  #   if len(self.postal_code) != pincode:
  #     raise ValueError(f"Invalid postal code length for country {self.country} it should be {pincode}")

class EmployeeCreate(BaseModel):
  name: str = Field(min_length=2)
  email: EmailStr
  age: int = Field(ge=18, le=65)
  address: AddressCreate | None = Field(default=None, Nullable=True)
  password: str = Field(min_length=8)

class EmployeePatch(BaseModel):
  name: str | None = Field(min_length=2, default=None)
  email: EmailStr | None = Field(default=None)
  age: int | None = Field(default=None, ge=18, le=65)




class AddressResponse(BaseModel):
  id: int
  employee_id : int
  street: str
  city: str
  country: str
  postal_code: str

  model_config=ConfigDict(from_attributes=True)


class AddressPatch(BaseModel):
    street: str | None = Field(default=None, min_length=3)
    city: str | None = Field(default=None, min_length=3)
    country: str | None = Field(default=None, min_length=3)
    postal_code: str | None = Field(default=None, min_length=3)

class EmployeeResponse(BaseModel):
  id: int
  name: str
  email: EmailStr
  age: int

  model_config=ConfigDict(from_attributes=True)