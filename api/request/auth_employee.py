from marshmallow import Schema, fields

from api.base import RequestDto


class RequestAuthEmployeeDtoSchema(Schema):
    login = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)


class RequestAuthEmployeeDto(RequestDto, RequestAuthEmployeeDtoSchema):
    __schema__ = RequestAuthEmployeeDtoSchema

