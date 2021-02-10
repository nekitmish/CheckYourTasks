from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.exceptions import ApiResponseValidationException
from api.response import ResponseMessageDto
from db.database import DBSession
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicMessagesNotFound, SanicBadRequest


class SortMessagesEndpoint(BaseEndpoint):

    async def method_get(self, request: Request, body: dict, session: DBSession,
                         token: dict, *args, **kwargs) -> BaseHTTPResponse:

        if 'recipient_login' in request.args:
            login = request.args['recipient_login'][0]
            db_message = message_queries.get_messages_by_recipient_login(session, token.get('eid'), login)
        elif 'recipient_id' in request.args:
            rid = request.args['recipient_id'][0]
            db_message = message_queries.get_messages_by_recipient_id(session, token.get('eid'), rid)
        elif 'sender_login' in request.args:
            login = request.args['sender_login'][0]
            db_message = message_queries.get_messages_by_sender_login(session, token.get('eid'), login)
        elif 'sender_id' in request.args:
            sid = request.args['sender_id'][0]
            db_message = message_queries.get_messages_by_sender_id(session, token.get('eid'), sid)
        else:
            raise SanicBadRequest('Bad request')

        try:
            response_model = ResponseMessageDto(db_message, many=True)
        except ApiResponseValidationException:
            raise SanicMessagesNotFound('Messages not found')

        return await self.make_response_json(body=response_model.dump(), status=200)
