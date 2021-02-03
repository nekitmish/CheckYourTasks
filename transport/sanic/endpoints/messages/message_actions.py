from sanic.request import Request
from sanic.response import BaseHTTPResponse
from ...exceptions import SanicMessagesNotFound, SanicDBException

from api.request.patch_message import RequestPatchMessageDto
from api.response.create_message import ResponseCreateMessageDto
from db.database import DBSession
from db.queries import message as message_queries
from db.exceptions import DBMessageNotExistsException, DBDataException, DBIntegrityException
from transport.sanic.endpoints import BaseEndpoint


class MessageActionEndpoint(BaseEndpoint):
    async def method_patch(self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args,
                           **kwargs) -> BaseHTTPResponse:
        try:
            sender_id = session.get_message_by_id(message_id).sender_id
        except DBMessageNotExistsException:
            raise SanicMessagesNotFound('')

        if token.get('eid') != sender_id:
            return await self.make_response_json(status=403)

        request_model = RequestPatchMessageDto(body)

        try:
            message = message_queries.patch_message(session, request_model, message_id)
        except DBMessageNotExistsException:
            raise SanicMessagesNotFound

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseCreateMessageDto(message)

        return await self.make_response_json(body=response_model.dump(), status=200)

    async def method_delete(self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args, **kwargs) -> BaseHTTPResponse:

        try:
            sender_id = session.get_message_by_id(message_id).sender_id
        except DBMessageNotExistsException:
            raise SanicMessagesNotFound('')

        if token.get('eid') != sender_id:
            return await self.make_response_json(status=403)

        try:
            message_queries.delete_message(session, message_id=message_id)
        except DBMessageNotExistsException:
            raise SanicMessagesNotFound('Message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)

    async def method_get(self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args,
                           **kwargs) -> BaseHTTPResponse:
        try:
            recipient_id = session.get_message_by_id(message_id).recipient_id
        except DBMessageNotExistsException:
            raise SanicMessagesNotFound('')

        if token.get('eid') != recipient_id:
            return await self.make_response_json(status=403)

        try:
            message = message_queries.get_message(session, message_id)
        except DBMessageNotExistsException:
            raise SanicMessagesNotFound('Message not found')

        response_model = ResponseCreateMessageDto(message)
        return await self.make_response_json(body=response_model.dump(), status=200)











