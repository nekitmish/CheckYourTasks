from sanic.request import Request
from sanic.response import BaseHTTPResponse, json
from http import HTTPStatus
from typing import Iterable

from configs.config import ApplicationConfig
from context import Context
from db.exceptions import DBEmployeeNotExistsException
from helpers.auth import read_token, ReadTokenException
from transport.sanic.exceptions import SanicAuthException
from db.database import DBSession


class SanicEndpoint:

    async def __call__(self, request: Request, *args, **kwargs):

        if self.auth_required:
            try:
                token = {
                    'token': self.import_body_auth(request)
                }
            except SanicAuthException as e:
                return await self.make_response_json(status=e.status_code)
            else:
                kwargs.update(token)
        return await self.handler(request, *args, **kwargs)

    def __init__(
            self,
            config: ApplicationConfig,
            context: Context,
            uri: str,
            methods: Iterable,
            auth_required: bool = False,
            *args, **kwargs):
        self.config = config
        self.context = context
        self.uri = uri
        self.methods = methods
        self.auth_required = auth_required
        self.__name__ = self.__class__.__name__

    @staticmethod
    async def make_response_json(
            body: dict = None, status: int = 200, message: str = None, error_code: int = None
    ) -> BaseHTTPResponse:
        if body is None:
            body = {
                'message': message or HTTPStatus(status).phrase,
                'error_code': error_code or status,
            }

        return json(body=body, status=status)

    @staticmethod
    def import_body_headers(request: Request) -> dict:
        return {
            header: value
            for header, value in request.headers.items()
            if header.lower().startswith('x-')
        }

        return headers

    @staticmethod
    def import_body_auth(request: Request) -> dict:
        token = request.headers.get('Authorization')
        try:
            return read_token(token)
        except ReadTokenException as e:
            raise SanicAuthException(str(e))

    @staticmethod
    def import_body_json(request: Request) -> dict:
        if 'application/json' in request.content_type and request.json is not None:
            return dict(request.json)
        return {}

    async def handler(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        body = {}

        body.update(self.import_body_json(request))
        body.update(self.import_body_headers(request))

        return await self._method(request, body, *args, **kwargs)

    async def _method(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        method = request.method.lower()
        func_name = f'method_{method}'

        if hasattr(self, func_name):
            func = getattr(self, func_name)
            return await func(request, body, *args, **kwargs)
        return await self.method_not_impl(method=method)

    async def method_not_impl(self, method: str) -> BaseHTTPResponse:
        return await self.make_response_json(status=500, message=f'Method {method.upper()} is not implemented')

    async def method_get(self, request: Request, body: dict, *args, **kwargs):
        return await self.method_not_impl('GET')

    async def method_post(self, request: Request, body: dict, *args, **kwargs):
        return await self.method_not_impl('POST')

    async def method_patch(self, request: Request, body: dict, *args, **kwargs):
        return await self.method_not_impl('PATCH')

    async def method_delete(self, request: Request, body: dict, *args, **kwargs):
        return await self.method_not_impl('DELETE')





