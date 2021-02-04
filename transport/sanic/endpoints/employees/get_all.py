from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response import ResponseAllEmployeesDto
from db.database import DBSession
from db.queries import employee as employee_queries
from transport.sanic.endpoints import BaseEndpoint


class AllEmployeeEndpoint(BaseEndpoint):

    async def method_get(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:

        db_employee = employee_queries.get_employees(session)
        response_model = ResponseAllEmployeesDto(db_employee, many=True)

        return await self.make_response_json(status=200, body=response_model.dump())
