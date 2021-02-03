from marshmallow import Schema, fields

from api.base import RequestDto


class RequestCreateEmployeeDtoSchema(Schema):
    login = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)
    position = fields.Str(missing=None)
    department = fields.Str(missing=None)


class RequestCreateEmployeeDto(RequestDto, RequestCreateEmployeeDtoSchema):
    __schema__ = RequestCreateEmployeeDtoSchema
