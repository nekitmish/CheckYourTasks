from marshmallow import Schema, fields

from api.base import RequestDto


class RequestMessageDtoSchema(Schema):
    recipient = fields.Str(required=True, nullable=False)
    message = fields.Str(required=True, nullable=False)


class RequestMessageDto(RequestDto, RequestMessageDtoSchema):
    __schema__ = RequestMessageDtoSchema
