import pytest

from exceptions import NotFoundException
from models.department import Department
from departments import service as department_service


async def test_get_by_name_returns_seeded_employee(db_session):

    # Seed a row directly via the ORM. We construct Employee ourselves
    # (with a real `password_hash`) because service.create currently
    # drops the password field — bypassing it keeps this test focused.
    seeded = Department(
        name="Engineering",
    )
    # `add()` is sync — it just stages the row in the session.
    db_session.add(seeded)
    # `commit()` is the IO step. Must be awaited.

    await db_session.commit()

    # `refresh()` re-reads the row so `seeded.id` is populated.

    await db_session.refresh(seeded)

    # Call the function under test — async, so we await.

    fetched = await department_service.get_department(seeded.id, db_session)

    assert fetched.id is not None
    assert fetched.name == seeded.name


async def test_get_by_id_raises_for_unknown_id(db_session):

    with pytest.raises(NotFoundException) as exc_info:
        await department_service.get_department(9999, db_session)

    assert "9999" in exc_info.value.detail
