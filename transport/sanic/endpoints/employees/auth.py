from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response.auth_employee import ResponseAuthEmployeeDto, AuthResponseObject
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicEmployeeNotFound, SanicPasswordHashException

from api.request import RequestAuthEmployeeDto

from helpers.password import check_hash, CheckPasswordHashException

from db.queries import employee as employee_queries
from db.exceptions import DBEmployeeNotExistsException

from helpers.auth import create_token


class AuthEmployeeEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestAuthEmployeeDto(body)

        try:
            db_employee = employee_queries.get_employee(session, login=request_model.login)
        except DBEmployeeNotExistsException:
            raise SanicEmployeeNotFound('Employee not found')

        try:
            check_hash(request_model.password, db_employee.password)
        except CheckPasswordHashException:
            raise SanicPasswordHashException('Wrong password')

        payload = {
            'eid': db_employee.id,
        }

        token = create_token(payload)
        response = AuthResponseObject(token)

        response_model = ResponseAuthEmployeeDto(response)

        return await self.make_response_json(
            body=response_model.dump(),
            status=200,
        )

