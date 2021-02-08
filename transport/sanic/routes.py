from transport.sanic import endpoints
from context import Context
from configs.config import ApplicationConfig
from typing import Tuple


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return (
        endpoints.HealthEndpoint(
            config=config, context=context, uri='/', methods=['GET', 'POST']),
        endpoints.CreateEmployeeEndpoint(
            config, context, uri='/employee', methods=['POST']),
        endpoints.AuthEmployeeEndpoint(
            config, context, uri='/employee/auth', methods=['POST']),
        endpoints.EmployeeEndpoint(
            config, context, uri='/employee/<eid:int>', methods=['PATCH', 'DELETE'], auth_required=True),
        endpoints.AllEmployeeEndpoint(
            config, context, uri='/employee/all', methods=['GET'], auth_required=True),
        endpoints.MyEmployeeEndpoint(
            config, context, uri='/employee', methods=['GET'], auth_required=True),
        endpoints.GetMyEmployeeByLoginEndpoint(
            config, context, uri='/employee/<login:string>', methods=['GET'], auth_required=True),
        endpoints.MessageEndpoint(
            config, context, uri='/msg', methods=['GET', 'POST'], auth_required=True),
        endpoints.MessageActionEndpoint(
            config, context, uri='/msg/<message_id:int>', methods=['PATCH', 'DELETE', 'GET'], auth_required=True),
        endpoints.SortMessagesBySenderLoginEndpoint(
            config, context, uri='/msg/from/<login:string>', methods=['GET'], auth_required=True),
        endpoints.SortMessagesBySenderIDEndpoint(
            config, context, uri='/msg/from/<sender_id:int>', methods=['GET'], auth_required=True),
        endpoints.SortMessagesByRecipientLoginEndpoint(
            config, context, uri='/msg/to/<login:string>', methods=['GET'], auth_required=True),
        endpoints.SortMessagesByRecipientIDEndpoint(
            config, context, uri='/msg/to/<recipient_id:int>', methods=['GET'], auth_required=True),




    )
