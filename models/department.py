from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Entity, Employee

class Department(Entity):


    name: Mapped[str] = mapped_column(String(50), nullable=False)

    employees: Mapped["employees"] = relationship("Employee", back_populates="employees")