from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.sanic.endpoints import BaseEndpoint
from api.request import RequestCreateEmployeeDto
from api.response import ResponseEmployeeDto
from transport.sanic.exceptions import SanicPasswordHashException, SanicDBException, SanicEmployeeConflictException

from db.queries import employee as employee_queries
from db.exceptions import DBDataException, DBIntegrityException, DBEmployeeExistsException

from helpers.password import generate_hash
from helpers.password import GeneratePasswordHashException


class CreateEmployeeEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateEmployeeDto(body)

        try:
            hashed_password = generate_hash(request_model.password)
        except GeneratePasswordHashException as e:
            raise SanicPasswordHashException(str(e))

        try:
            db_employee = employee_queries.create_employee(session, request_model, hashed_password)
        except DBEmployeeExistsException:
            raise SanicEmployeeConflictException('Login is busy')

        try:
            session.commit_session()
        except(DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseEmployeeDto(db_employee)

        return await self.make_response_json(body=response_model.dump(), status=201)
