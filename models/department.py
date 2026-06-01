from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Entity

employee_departments = Table(
    "employee_departments",
    Entity.metadata,
    Column("employee_id", ForeignKey("employees.id"), primary_key=True),
    Column("department_id", ForeignKey("departments.id"), primary_key=True),
)


class Department(Entity):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    employees: Mapped[list["Employee"]] = relationship(
        "Employee", back_populates="departments", secondary="employee_departments"
    )
