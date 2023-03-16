from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from calculator.exceptions import OperationServiceProblem, OperationInvalid
from calculator.operations import OPERATIONS_MAP
from calculator.schemas import OperationRequest


class Operation(models.Model):
    type = models.CharField("Operation type", max_length=100)
    cost = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return self.type

    @classmethod
    def get_operator_by_request(cls, request_operator: OperationRequest) -> "Operation":
        try:
            operator_id = OPERATIONS_MAP[request_operator.operator]["id"]
            return cls.objects.get(id=operator_id)
        except KeyError:
            raise OperationInvalid(f"Invalid operation: {request_operator.operator}")
        except ObjectDoesNotExist:
            raise OperationServiceProblem(
                f"Operator {request_operator.operator} is not supported."
            )


class Record(models.Model):
    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE, related_name="records"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="records"
    )
    amount = models.DecimalField(max_digits=7, decimal_places=3)
    user_balance = models.DecimalField(max_digits=7, decimal_places=3)
    operation_response = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
