from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto
from api.response import ResponseCreateMessageDto
from api.exceptions import ApiResponseValidationException
from db.database import DBSession
from db.exceptions import DBEmployeeNotExistsException, DBDataException, DBIntegrityException
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicEmployeeNotFound, SanicDBException, SanicMessagesNotFound


class MessageEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
                          ) -> BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)

        try:
            rid = session.get_employee_id_by_login(request_model.recipient)
            sid = token.get('eid')
            db_message = message_queries.create_message(session, request_model, rid, sid)
        except DBEmployeeNotExistsException:
            raise SanicEmployeeNotFound('Employee not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseCreateMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

    async def method_get(self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
                         ) -> BaseHTTPResponse:

        db_message = message_queries.get_messages(session, token.get('eid'))
        try:
            response_model = ResponseCreateMessageDto(db_message, many=True)
        except ApiResponseValidationException:
            raise SanicMessagesNotFound('Messages not found')

        return await self.make_response_json(body=response_model.dump(), status=200)




