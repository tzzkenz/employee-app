from pydantic import BaseModel, ConfigDict, Field


class DepartmentCreate(BaseModel):
  name: str = Field(min_length=3)

class DepartmentResponse(BaseModel):
  id: int
  name: str

  model_config=ConfigDict(from_attributes=True)

class DepartmentPatch(BaseModel):
  name: str | None = Field(default=False)
