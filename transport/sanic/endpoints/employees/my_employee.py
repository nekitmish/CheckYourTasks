from sanic.request import Request
from sanic.response import BaseHTTPResponse

from db.database import DBSession
from api.response import ResponseEmployeeDto
from db.exceptions import DBEmployeeNotExistsException
from db.queries import employee as employee_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicEmployeeNotFound


class MyEmployeeEndpoint(BaseEndpoint):

    async def method_get(self, request: Request, body: dict, session: DBSession, eid: int, token: dict, *args, **kwargs
                         ) -> BaseHTTPResponse:

        if token.get('eid') != eid:
            return await self.make_response_json(status=403)

        try:
            db_employee = employee_queries.get_employee(session, employee_id=eid)
        except DBEmployeeNotExistsException:
            raise SanicEmployeeNotFound('User not found')

        response_model = ResponseEmployeeDto(db_employee)

        return await self.make_response_json(body=response_model.dump(), status=202)
