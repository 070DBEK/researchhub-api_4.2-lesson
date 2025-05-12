from common.exceptions import ObjectNotFound
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        customized_response = {"errors": []}
        data = response_data_handler(response.data)
        for key, value in data.items():
            error = {"field": key, "message": value}
            customized_response["errors"].append(error)
        response.data = customized_response
    return response


def response_data_handler(data):
    if isinstance(data, list):
        data = {"non_field_errors": data}

    detail = data.get("detail", None)
    if detail is not None:
        match detail.code.lower():
            case "not_found":
                error_detail = ErrorDetail(ObjectNotFound.default_detail)
                error_detail.code = ObjectNotFound.default_code
            case _:
                error_detail = ErrorDetail(detail)
                error_detail.code = detail.code
        data = {"non_field_errors": [error_detail]}
    return data
