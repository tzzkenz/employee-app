import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


from database import Base
from employees import service as employee_service
from employees.schema import EmployeeCreate

@pytest.mark.asyncio
async def test_create_employee_persists_the_record():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession)

    async with session_factory() as db:
        body = EmployeeCreate(
            name="Ada",
            email="ada@example.com",
            password="Secret123@awewe",
            age=20
        )
        employee = await  employee_service.create_employee(body, db)
        

        assert employee.id is not None
        assert employee.name == "Ada"
        assert employee.email == "ada@example.com"
        assert employee.age == 20

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()