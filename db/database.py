from typing import List

from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session, sessionmaker, Query

from db.models import BaseModel, DBEmployee, DBMessage
from db.exceptions import DBIntegrityException, DBDataException, DBEmployeeNotExistsException, DBMessageNotExistsException


class DBSession:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def query(self, *args, **kwargs) -> Query:
        return self._session.query(*args, **kwargs)

    def employees(self) -> Query:
        return self.query(DBEmployee).filter(DBEmployee.is_delete == False)

    def messages(self, employee_id: int) -> Query:
        return self.query(DBMessage).filter(DBMessage.recipient_id == employee_id)

    def messages_not_deleted(self) -> Query:
        return self.query(DBMessage).filter(DBMessage.is_delete == False)

    def close_session(self):
        self._session.close()

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

    def get_employee_by_login(self, login: str) -> DBEmployee:
        employee = self.employees().filter(DBEmployee.login == login).first()
        return employee

    def get_employee_by_id(self, eid: int) -> DBEmployee:
        employee = self.employees().filter(DBEmployee.id == eid).first()
        if employee is None:
            raise DBEmployeeNotExistsException('Your employee not found')
        return employee

    def get_employee_id_by_login(self, login: str) -> int:
        employee = self.get_employee_by_login(login)
        return employee.id

    def get_employee_all(self) -> List['DBEmployee']:
        qs = self.employees()
        print(qs)
        return qs.all()

    def get_message_all(self, rid: int) -> List['DBMessage']:
        return self.messages(rid).filter(DBMessage.is_delete == False).all()

    def get_message_by_id(self, message_id: int) -> DBMessage:
        msg = self.messages_not_deleted().filter(DBMessage.id == message_id).first()
        if msg is None:
            raise DBMessageNotExistsException('Error')
        return msg

    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

        if need_close:
            self.close_session()


class Database:
    connection: Engine
    session_factory: sessionmaker
    _test_query = 'SELECT 1'
    session: Session

    def __init__(self, connection: Engine):
        self.connection = connection
        self.session_factory = sessionmaker(bind=self.connection)
        self.session = None

    def check_connection(self):
        self.connection.execute(self._test_query).fetchone()

    def make_session(self) -> DBSession:
        session = self.session_factory()
        return DBSession(session)
