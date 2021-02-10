from typing import List

from transport.sanic.exceptions import SanicEmployeeNotFound
from api.request import RequestCreateMessageDto
from db.database import DBSession
from db.exceptions import DBEmployeeNotExistsException, DBMessageNotExistsException
from db.models import DBMessage
from db.queries.employee import get_employee_id_by_login


def create_message(session: DBSession, message: RequestCreateMessageDto, sid: int) -> DBMessage:

    rid = get_employee_id_by_login(session, message.recipient)

    try:
        session.get_employee_by_id(rid)
    except DBEmployeeNotExistsException:
        raise SanicEmployeeNotFound('Employee not found')

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

