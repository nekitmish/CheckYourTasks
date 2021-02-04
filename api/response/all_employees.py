from marshmallow import Schema, fields

from api.base import ResponseDto


class ResponseAllEmployeesDtoSchema(Schema):
    id = fields.Int(required=True)
    login = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    position = fields.Str(required=True, allow_none=True)
    department = fields.Str(required=True, allow_none=True)


class ResponseAllEmployeesDto(ResponseDto):
    __schema__ = ResponseAllEmployeesDtoSchema
