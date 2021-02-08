from typing import List

from api.request import RequestMessageDto
from db.database import DBSession
from db.exceptions import DBEmployeeNotExistsException, DBMessageNotExistsException
from db.models import DBMessage


def create_message(session: DBSession, message: RequestMessageDto, rid: int, sid: int) -> DBMessage:

    if session.get_employee_by_id(rid) is None:
        raise DBEmployeeNotExistsException('Employee does not exists')

    new_message = DBMessage(
        sender_id=sid,
        recipient_id=rid,
        message=message.message,
    )

    session.add_model(new_message)

    return new_message


def get_messages(session: DBSession, rid: int) -> List['DBMessage']:
    return session.get_message_all(rid)


def get_messages_by_sender_login(session: DBSession, rid: int, login: str) -> List['DBMessage']:
    return session.get_messages_by_sender_login(rid, login)


def get_messages_by_sender_id(session: DBSession, rid: int, sender_id: int) -> List['DBMessage']:
    return session.get_messages_by_sender_id(rid, sender_id)


def get_messages_by_recipient_id(session: DBSession, sender_id: int, recipient_id: int) -> List['DBMessage']:
    return session.get_messages_by_recipient_id(sender_id, recipient_id)


def get_messages_by_recipient_login(session: DBSession, sender_id: int, login: str) -> List['DBMessage']:
    return session.get_messages_by_recipient_login(sender_id, login)


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
    return db_message


def get_message(session: DBSession, message_id: int) -> DBMessage:
    db_message = session.get_message_by_id(message_id)
    return db_message

