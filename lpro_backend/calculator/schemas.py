from typing import List, Optional

from ninja import Schema


class AvailableOperationResponse(Schema):
    text: str
    param_count: int


class OperationRequest(Schema):
    operator: str
    params: List[int]


class OperationResponse(Schema):
    ok: bool = True
    result: str
