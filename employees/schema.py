from datetime import datetime
import re
from datetime import timezone
from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

from exceptions import BadRequestException
from models import employee
from models.employee import EmployeeRole, EmployeeStatus



class AddressCreate(BaseModel):
    street: str = Field(min_length=3)
    city: str = Field(min_length=3)
    country: str = Field(min_length=2)
    postal_code: str = Field(min_length=3)

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, value: str) -> str:
        if not value.isdigit():
            raise BadRequestException("postal_code value should be a digit (0-9)")
        return value

    @model_validator(mode="after")
    def postal_code_length_for_country(self):
        pincodes = {"US": 5, "IN": 6}

        pincode = pincodes.get(self.country, None)
        if pincode is None:
            raise BadRequestException("Not a valid country")

        if len(self.postal_code) != pincode:
            raise BadRequestException(
                f"Invalid postal code length for country {self.country} it should be {pincode}"
            )

        return self


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    age: int = Field(ge=18, le=65)
    address: AddressCreate | None = Field(
        default=None, json_schema_extra={"nullable": True}
    )
    password: str = Field(min_length=8)
    role: EmployeeRole
    status: EmployeeStatus

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$")
        if not pattern.match(value):
            raise BadRequestException(
                "Password must contain at least 8 characters, "
                "one uppercase letter, one lowercase letter, "
                "one digit, and one special character."
            )
        return value


class EmployeePatch(BaseModel):
    name: str | None = Field(min_length=2, default=None)
    email: EmailStr | None = Field(default=None)
    age: int | None = Field(default=None, ge=18, le=65)
    status: EmployeeStatus

    model_config = ConfigDict(extra='allow')

    @model_validator(mode="after")
    def validate_status_vs_experience(self):
        time = datetime.fromisoformat(self.created_at)
        if self.status and time:
            print("hitttttt", type(time))
            experience = (datetime.now(timezone.utc) - time).days
            if experience < 6 and self.status not in ( EmployeeStatus.PROBATION, EmployeeStatus.INACTICE):
                raise BadRequestException("BAAAAD")
        return self
    



class AddressResponse(BaseModel):
    id: int
    employee_id: int
    street: str
    city: str
    country: str
    postal_code: str

    model_config = ConfigDict(from_attributes=True)


class AddressPatch(BaseModel):
    street: str | None = Field(default=None, min_length=3)
    city: str | None = Field(default=None, min_length=3)
    country: str | None = Field(default=None, min_length=2)
    postal_code: str | None = Field(default=None, min_length=3)

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, value: str) -> str:
        if not value.isdigit():
            raise BadRequestException("postal_code value should be a digit (0-9)")
        return value

    @model_validator(mode="after")
    def postal_code_length_for_country(self):
        pincodes = {"US": 5, "IN": 6}

        pincode = pincodes.get(self.country, None)
        if pincode is None:
            raise BadRequestException("Not a valid country")

        if len(self.postal_code) != pincode:
            raise BadRequestException(
                f"Invalid postal code length for country {self.country} it should be {pincode}"
            )

        return self


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    role: EmployeeRole
    created_at: datetime
    status: EmployeeStatus

    @computed_field
    @property
    def experience(self) -> float:
        now = datetime.now(timezone.utc)
        return round((now - self.created_at).days)
    model_config = ConfigDict(from_attributes=True)
