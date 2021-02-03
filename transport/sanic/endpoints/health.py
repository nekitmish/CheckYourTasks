from sanic.request import Request
from transport.sanic.base import SanicEndpoint


class HealthEndpoint(SanicEndpoint):
    async def method_get(self, request: Request, body: dict, *args, **kwargs):
        response = {
            'hello': 'world'
        }

        return await self.make_response_json(body=response, status=200)

    async def method_post(self, request: Request, body: dict, *args, **kwargs):
        return await self.make_response_json(body=request, status=200)
