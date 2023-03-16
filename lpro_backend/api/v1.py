from typing import Dict

from ninja import Router

from calculator.operations import get_api_operations, operate
from calculator.schemas import (
    AvailableOperationResponse,
    OperationRequest,
    OperationResponse,
)

v1_router = Router()


@v1_router.get("/operations", response=Dict[str, AvailableOperationResponse])
def available_operations(request):
    return get_api_operations()


@v1_router.post("/calculate", response=OperationResponse)
def calculate(request, operation: OperationRequest):
    result = operate(operation.operator, operation.params)
    return OperationResponse(result=result)
