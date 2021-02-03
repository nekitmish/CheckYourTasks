from sanic.exceptions import SanicException


class ApiValidationException(SanicException):
    status_code = 400


class ApiResponseValidationException(Exception):
    status_code = 500
