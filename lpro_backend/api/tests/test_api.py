import pytest
from unittest.mock import Mock
from typing import Any, Dict
from ninja.testing import TestClient
from django.contrib.auth import get_user_model
from oauth2_provider.models import get_application_model, get_access_token_model
from django.utils import timezone
from api import api
from django.core.management import call_command

User = get_user_model()
Application = get_application_model()
AccessToken = get_access_token_model()


class FixedTestClient(TestClient):
    def _build_request(
        self, method: str, path: str, data: Dict, request_params: Any
    ) -> Mock:
        request = super()._build_request(method, path, data, request_params)
        request.get_full_path.return_value = path
        return request


client = FixedTestClient(api)


@pytest.fixture(scope="session")
def django_populate_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "operations.json", verbosity=0)


@pytest.fixture
def get_user_and_token():
    user = User.objects.create_user("test@mail.com", "test")
    application = Application.objects.create(
        name="test application",
        redirect_uris="http://localhost:8000/callback",
        user=user,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
    )

    access_token = AccessToken.objects.create(
        user=user,
        application=application,
        token="secret-access-token-key",
        expires=timezone.now() + timezone.timedelta(minutes=10),
    )
    return user, access_token


@pytest.mark.django_db
def test_index():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_operations():
    response = client.get("/v1/operations")
    assert response.status_code == 200


@pytest.mark.django_db
def test_authenticated_api(get_user_and_token):
    user, access_token = get_user_and_token

    # unauthenticated access
    response = client.get("/v1/record")
    assert response.status_code == 401

    # authenticated access
    auth_bearer = "Bearer {}".format(access_token.token)
    response = client.get(
        "/v1/record",
        headers={"AUTHORIZATION": auth_bearer},
    )
    assert response.status_code == 200

    auth_bearer = "Bearer failed-bearer"
    response = client.get(
        "/v1/record",
        headers={"AUTHORIZATION": auth_bearer},
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_calculate_should_calculate(django_populate_fixtures, get_user_and_token):
    user, access_token = get_user_and_token
    user.balance = 1
    user.save()

    response = client.post(
        "/v1/calculate",
        json={"operator": "ADD", "params": [1, 2]},
        headers={"AUTHORIZATION": "Bearer {}".format(access_token.token)},
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_calculate_should_require_params(django_populate_fixtures, get_user_and_token):
    _, access_token = get_user_and_token

    response = client.post(
        "/v1/calculate",
        json={"params": [1, 2]},
        headers={"AUTHORIZATION": "Bearer {}".format(access_token.token)},
    )
    assert response.status_code == 422


@pytest.mark.django_db
def test_calculate_should_validate_operation(django_populate_fixtures, get_user_and_token):
    user, access_token = get_user_and_token
    user.balance = 1
    user.save()

    response = client.post(
        "/v1/calculate",
        json={"operator": "ERROR", "params": [1, 2]},
        headers={"AUTHORIZATION": "Bearer {}".format(access_token.token)},
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_calculate_should_validate_balance(django_populate_fixtures, get_user_and_token):
    user, access_token = get_user_and_token
    user.balance = 0
    user.save()

    response = client.post(
        "/v1/calculate",
        json={"operator": "ADD", "params": [1, 2]},
        headers={"AUTHORIZATION": "Bearer {}".format(access_token.token)},
    )
    assert response.status_code == 402

