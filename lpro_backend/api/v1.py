from typing import Dict, List, Optional, Any

from django.http import HttpRequest
from ninja import Router
from ninja.pagination import paginate
from ninja.security import HttpBearer
from oauth2_provider.views.mixins import OAuthLibMixin

from calculator.models import Record, Operation
from calculator.operations import get_api_operations, operate
from calculator.schemas import (
    AvailableOperationResponse,
    OperationRequest,
    OperationResponse,
    RecordResponse,
)
from core.models import User

v1_router = Router()


class AuthValidator(HttpBearer, OAuthLibMixin):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        is_verified, auth_request = self.verify_request(request)
        if not is_verified:
            return None
        return auth_request.user


@v1_router.get("/operations", response=Dict[str, AvailableOperationResponse])
def available_operations(request):
    return get_api_operations()


@v1_router.post("/calculate", auth=AuthValidator(), response=OperationResponse)
def calculate(request, operation_request: OperationRequest):
    user: User = request.auth
    operation = Operation.get_operator_by_request(operation_request)
    user.check_balance(operation.cost)
    result = operate(operation_request.operator, operation_request.params)
    user.discount(operation.cost)

    Record.objects.create(
        operation=operation,
        user=user,
        amount=operation.cost,
        user_balance=user.balance,
        operation_response=result,
    )
    return OperationResponse(result=result)


@v1_router.get("/record", auth=AuthValidator(), response=List[RecordResponse])
@paginate
def records(request):
    user: User = request.auth
    return user.records.select_related('operation').all()
