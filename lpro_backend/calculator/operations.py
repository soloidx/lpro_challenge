import inspect
import requests


def addition(num1: int, num2: int) -> int:
    return num1 + num2


def subtraction(num1: int, num2: int) -> int:
    return num1 - num2


def multiplication(num1: int, num2: int) -> int:
    return num1 * num2


def division(num1: int, num2: int) -> int:
    return num1 / num2


def square_root(num: int) -> float:
    return num ** 0.5


def random_string() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


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
    }
}
