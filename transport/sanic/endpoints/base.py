from sanic.request import Request
from sanic.response import BaseHTTPResponse
from sanic.exceptions import SanicException

from db.exceptions import DBEmployeeNotExistsException
from transport.sanic.base import SanicEndpoint
from transport.sanic.exceptions import SanicEmployeeNotFound
from db.database import DBSession


class BaseEndpoint(SanicEndpoint):
    async def _method(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:

        database = self.context.database
        session = database.make_session()

        if self.auth_required:
            try:
                DBSession(session).get_employee_by_id(kwargs.get('token').get('eid'))
            except DBEmployeeNotExistsException:
                raise SanicEmployeeNotFound('Your employee not found')

        try:
            return await super()._method(request, body, session, *args, **kwargs)

        except SanicException as e:
            return await self.make_response_json(status=e.status_code, message=str(e))

