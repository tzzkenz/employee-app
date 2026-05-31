from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

class AddressCreate(BaseModel):
  street: str
  city: str
  country: str
  postal_code: str

  # @field_validator('postal_code')
  # @classmethod
  # def validate_postal_code(cls, value: int) -> int:
  #   if not value.isdigit():
  #     raise ValueError("postal_code value should be a digit (0-9)")    
  #   return value
    
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
  age: int
  address: AddressCreate | None = Field(default=None, Nullable=True)

class EmployeePatch(BaseModel):
  name: str = Field(min_length=2, default=None)
  email: EmailStr = Field(default=None)
  age: int = Field(default=None)
  address: AddressCreate | None = Field(default=None, Nullable=True)




class AddressResponse(BaseModel):
  id: int
  employee_id : int
  street: str
  city: str
  country: str
  postal_code: str

  model_config=ConfigDict(from_attributes=True)


class AddressPatch(BaseModel):
  street: str = Field(default=None)
  city: str = Field(default=None)
  country: str = Field(default=None)
  postal_code: str = Field(default=None)

class EmployeeResponse(BaseModel):
  id: int
  name: str
  email: EmailStr
  age: int
  # address: list[AddressResponse] | None = Field(default=None)

  model_config=ConfigDict(from_attributes=True)