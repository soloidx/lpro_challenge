import pytest

from calculator import operations
from unittest import mock
from django.conf import settings
from calculator.operations import HTTPError


def test_addition():
    assert operations.addition(2, 3) == 5
    assert operations.addition(-2, 3) == 1
    assert operations.addition(0, 0) == 0


def test_subtraction():
    assert operations.subtraction(5, 3) == 2
    assert operations.subtraction(-2, -3) == 1
    assert operations.subtraction(0, 0) == 0


def test_multiplication():
    assert operations.multiplication(2, 3) == 6
    assert operations.multiplication(-2, 3) == -6
    assert operations.multiplication(0, 0) == 0


def test_division():
    assert operations.division(6, 3) == 2
    assert operations.division(7, 2) == 3.5
    assert operations.division(-6, 3) == -2
    with pytest.raises(operations.OperationInvalid):
        operations.division(5, 0)


def test_square_root():
    assert operations.square_root(4) == 2.0
    assert operations.square_root(25) == 5.0
    with pytest.raises(operations.OperationInvalid):
        operations.square_root(-1)


@mock.patch("calculator.operations.requests")
def test_random_string(requests_mock):
    settings.RANDOM_SERVICE_ENDPOINT = "https://localhost"
    get_mock = mock.Mock()
    requests_mock.get = get_mock
    get_mock.return_value = mock.Mock()
    get_mock.return_value.text = "12345"
    assert operations.random_string() == "12345"


@mock.patch("calculator.operations.requests")
def test_random_string_should_fail(requests_mock):
    settings.RANDOM_SERVICE_ENDPOINT = "https://localhost"
    get_mock = mock.Mock()
    requests_mock.get = get_mock
    get_mock.return_value.raise_for_status.side_effect = HTTPError

    with pytest.raises(operations.OperationServiceProblem):
        operations.random_string()


def test_get_api_operations():
    result = operations.get_api_operations()
    assert len(result) > 0


def test_operate_should_operate():
    result = operations.operate("ADD", [2, 3])
    assert result == "5"
    result = operations.operate("SUB", [2, 3])
    assert result == "-1"
    result = operations.operate("MUL", [2, 3])
    assert result == "6"
    result = operations.operate("DIV", [2, 3])
    assert result == "0.6666666666666666"
    result = operations.operate(
        "SQRT",
        [
            2,
        ],
    )
    assert result == "1.4142135623730951"
    with mock.patch("calculator.operations.requests") as requests_mock:
        requests_mock.get.return_value = mock.Mock()
        requests_mock.get.return_value.text = "12345"
        result = operations.operate("RANDOM", [])
        assert result == "12345"


def test_operate_should_raise_invalid_operation():
    with pytest.raises(operations.OperationInvalid):
        operations.operate("INVALID", [2, 3])


def test_operate_should_raise_invalid_input():
    with pytest.raises(operations.OperationInvalid):
        operations.operate("ADD", [])

    with pytest.raises(operations.OperationInvalid):
        operations.operate("ADD", [1, 2, 3])
