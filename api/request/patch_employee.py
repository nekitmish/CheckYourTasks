from marshmallow import Schema, fields

from api.base import RequestDto


class RequestPatchEmployeeDtoSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    position = fields.Str()
    department = fields.Str()


class RequestPatchEmployeeDto(RequestDto, RequestPatchEmployeeDtoSchema):
    fields: list
    __schema__ = RequestPatchEmployeeDtoSchema
    
    def __init__(self, *args, **kwargs):
        self.fields = []
        super(RequestPatchEmployeeDto, self).__init__(*args, **kwargs)
        
    def set(self, key, value):
        self.fields.append(key)
        super(RequestPatchEmployeeDto, self).set(key, value)
