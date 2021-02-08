from typing import List

from api.request import RequestCreateEmployeeDto
from db.database import DBSession
from db.exceptions import DBEmployeeExistsException, DBEmployeeNotExistsException
from db.models import DBEmployee


def create_employee(session: DBSession, employee: RequestCreateEmployeeDto, hashed_password: bytes) -> DBEmployee:
    new_employee = DBEmployee(
        login=employee.login,
        password=hashed_password,
        first_name=employee.first_name,
        last_name=employee.last_name,
        position=employee.position,
        department=employee.department,
    )

    if session.get_employee_by_login(new_employee.login) is not None:
        raise DBEmployeeExistsException

    session.add_model(new_employee)

    return new_employee


def get_employee(session: DBSession, *, login: str = None, employee_id: int = None) -> DBEmployee:
    db_employee = None

    if login is not None:
        db_employee = session.get_employee_by_login(login)

    elif employee_id is not None:
        db_employee = session.get_employee_by_id(employee_id)

    if db_employee is None:
        raise DBEmployeeNotExistsException('Employee does not exists')
    return db_employee


def patch_employee(session: DBSession, employee, employee_id: int) -> DBEmployee:

    db_employee = session.get_employee_by_id(employee_id)
    for attr in employee.fields:
        if hasattr(employee, attr):
            value = getattr(employee, attr)
            setattr(db_employee, attr, value)

    return db_employee


def delete_employee(session: DBSession, employee_id: int) -> DBEmployee:
    db_employee = session.get_employee_by_id(employee_id)
    db_employee.is_delete = True
    return db_employee


def get_employees(session: DBSession) -> List['DBEmployee']:
    return session.get_employee_all()


def get_employee_id_by_login(session: DBSession, login: str) -> int:
    return session.get_employee_id_by_login(login)


