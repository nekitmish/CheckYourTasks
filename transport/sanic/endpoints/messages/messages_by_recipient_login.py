from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.exceptions import ApiResponseValidationException
from api.response import ResponseCreateMessageDto
from db.database import DBSession
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicMessagesNotFound


class SortMessagesByRecipientLoginEndpoint(BaseEndpoint):

    async def method_get(self, request: Request, body: dict, session: DBSession, login: str,
                         token: dict, *args, **kwargs) -> BaseHTTPResponse:

        db_message = message_queries.get_messages_by_recipient_login(session, token.get('eid'), login)
        try:
            response_model = ResponseCreateMessageDto(db_message, many=True)
        except ApiResponseValidationException:
            raise SanicMessagesNotFound

        return await self.make_response_json(body=response_model.dump(), status=200)
