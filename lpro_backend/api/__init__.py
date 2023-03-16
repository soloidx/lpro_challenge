from ninja import NinjaAPI

from api.v1 import v1_router
from calculator.exceptions import OperationInvalid, OperationServiceProblem, OperationRateLimitExceeded

api = NinjaAPI(csrf=True)


@api.get("/")
def index(request):
    return {"status": "ok"}


api.add_router("/v1/", v1_router)


def simple_error_response(msg, *, err_type="value_error"):
    return {
        "detail": [
            {
                "loc": ["body"],
                "msg": msg,
                "type": err_type,
            }
        ]
    }


@api.exception_handler(OperationInvalid)
def handle_invalid_operation(request, exc):
    return api.create_response(request, simple_error_response(str(exc)), status=400)


@api.exception_handler(OperationServiceProblem)
def handle_service_problem(request, exc):
    return api.create_response(
        request, simple_error_response(str(exc), err_type="internal_error"), status=500
    )


@api.exception_handler(OperationRateLimitExceeded)
def handle_rate_limit(request, exc):
    return api.create_response(
        request, simple_error_response(str(exc), err_type="user_error"), status=402
    )
