from sanic.exceptions import SanicException

from api.base import ResponseDto


class ValidationError(SanicException):
    status_code = 400


class ResponseAuthEmployeeDtoSchema:

    def __init__(self, *args, **kwargs):
        self.fields = {'Authorization': ''}

    def load(self, data: dict) -> dict:

        valid_data = {}

        for key, value in data.items():
            if key not in self.fields:
                continue
            if not isinstance(value, self.fields[key].__class__):
                raise ValidationError(f'{key} should be a str')

            valid_data[key] = value

        return valid_data


class ResponseAuthEmployeeDto(ResponseDto):
    __schema__ = ResponseAuthEmployeeDtoSchema


class AuthResponseObject:
    def __init__(self, token):
        self.Authorization = token




