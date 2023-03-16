from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from ninja import Schema, Field


class AvailableOperationResponse(Schema):
    text: str
    param_count: int


class OperationRequest(Schema):
    operator: str
    params: List[int]


class OperationResponse(Schema):
    ok: bool = True
    result: str


class RecordResponse(Schema):
    operation_id: int
    operation: str = Field(..., alias="operation.type")
    amount: Decimal
    user_balance: Decimal
    operation_response: str
    date: datetime

