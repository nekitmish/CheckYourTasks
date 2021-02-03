from marshmallow import Schema, fields

from api.base import RequestDto


class RequestPatchMessageDtoSchema(Schema):
    message = fields.Str()


class RequestPatchMessageDto(RequestDto, RequestPatchMessageDtoSchema):
    fields: list
    __schema__ = RequestPatchMessageDtoSchema

    def __init__(self, *args, **kwargs):
        self.fields = []
        super(RequestPatchMessageDto, self).__init__(*args, **kwargs)

    def set(self, key, value):
        self.fields.append(key)
        super(RequestPatchMessageDto, self).set(key, value)