import inspect
from math import sqrt

import requests
from django.conf import settings
from requests.exceptions import HTTPError

from calculator.exceptions import OperationInvalid, OperationServiceProblem


def addition(num1: int, num2: int) -> int:
    return num1 + num2


def subtraction(num1: int, num2: int) -> int:
    return num1 - num2


def multiplication(num1: int, num2: int) -> int:
    return num1 * num2


def division(num1: int, num2: int) -> int:
    try:
        result = num1 / num2
    except ZeroDivisionError:
        raise OperationInvalid("Cannot divide by zero")
    return result


def square_root(num: int) -> float:
    try:
        result = sqrt(num)
    except ValueError:
        raise OperationInvalid("The number is invalid")
    return result


def random_string() -> str:
    # get a random string from random.com
    url = "".join(
        [
            settings.RANDOM_SERVICE_ENDPOINT,
            f"/strings/?num=1&len={settings.RANDOM_STRING_LENGTH}",
            "&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new",
        ]
    )
    response = requests.get(url)
    try:
        response.raise_for_status()
        return response.text.strip()
    except HTTPError:
        raise OperationServiceProblem(
            "There was a problem with the random string service"
        )


OPERATIONS_MAP = {
    "ADD": {
        "fn": addition,
        "id": 1,
        "text": "+",
        "param_count": len(inspect.signature(addition).parameters),
    },
    "SUB": {
        "fn": subtraction,
        "id": 2,
        "text": "-",
        "param_count": len(inspect.signature(subtraction).parameters),
    },
    "MUL": {
        "fn": multiplication,
        "id": 3,
        "text": "*",
        "param_count": len(inspect.signature(multiplication).parameters),
    },
    "DIV": {
        "fn": division,
        "id": 4,
        "text": "/",
        "param_count": len(inspect.signature(division).parameters),
    },
    "SQRT": {
        "fn": square_root,
        "id": 5,
        "text": "sqrt",
        "param_count": len(inspect.signature(square_root).parameters),
    },
    "RANDOM": {
        "fn": random_string,
        "id": 6,
        "text": "random",
        "param_count": len(inspect.signature(random_string).parameters),
    },
}


def get_api_operations() -> dict:
    return {
        key: {
            "text": val["text"],
            "param_count": val["param_count"],
        }
        for key, val in OPERATIONS_MAP.items()
    }


def operate(operation_key: str, params: list) -> str:
    if operation_key not in OPERATIONS_MAP:
        raise OperationInvalid(f"Invalid operation: {operation_key}")
    operation = OPERATIONS_MAP[operation_key]
    if len(params) != operation["param_count"]:
        raise OperationInvalid(f"Invalid number of parameters: {len(params)}")
    return str(operation["fn"](*params))
