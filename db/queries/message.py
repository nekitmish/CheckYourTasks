from typing import List

from api.request import RequestCreateMessageDto
from db.database import DBSession
from db.exceptions import DBEmployeeNotExistsException, DBMessageNotExistsException
from db.models import DBMessage


def create_message(session: DBSession, message: RequestCreateMessageDto, rid: int, sid: int) -> DBMessage:
    new_message = DBMessage(
        sender_id=sid,
        recipient_id=rid,
        message=message.message,
    )

    if session.get_employee_by_id(rid) is None:
        raise DBEmployeeNotExistsException('Employee does not exists')

    session.add_model(new_message)

    return new_message


def get_messages(session: DBSession, rid: int) -> List['DBMessage']:
    return session.get_message_all(rid)


def get_messages_by_sender_login(session: DBSession, rid: int, login: str) -> List['DBMessages']:
    return session.get_messages_by_sender_login(rid, login)


def patch_message(session: DBSession, message, message_id: int) -> DBMessage:
    db_message = session.get_message_by_id(message_id)

    for attr in message.fields:
        if hasattr(message, attr):
            value = getattr(message, attr)
            setattr(db_message, attr, value)

    return db_message


def delete_message(session: DBSession, message_id: int):
    db_message = session.get_message_by_id(message_id)
    db_message.is_delete = True


def get_message(session: DBSession, message_id: int) -> DBMessage:
    db_message = session.get_message_by_id(message_id)
    return db_message

