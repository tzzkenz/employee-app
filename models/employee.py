from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Entity
from models.department import employee_departments

class Employee(Entity):
  __abstract__ = False
  __tablename__ = "employees"

  name: Mapped[str] = mapped_column(String(50), nullable=False)
  email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
  age: Mapped[int] = mapped_column(Integer, nullable=False)

  addresses: Mapped[list["Address"]] = relationship("Address", back_populates="employee", cascade="all, delete-orphan")

  departments: Mapped[list["Department"]] = relationship("Department", secondary=employee_departments, back_populates="employees")
  password_hash: Mapped[str] = mapped_column(String(), nullable=False)