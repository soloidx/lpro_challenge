from core.models import User
import pytest
from calculator.exceptions import OperationRateLimitExceeded


@pytest.mark.django_db
def test_create_user():
    email = "efpyi@example.com"
    password = "testpass123"
    user = User.objects.create_user(
        email=email,
        password=password
    )

    assert user.email == email
    assert user.check_password(password)


@pytest.mark.django_db
def test_create_superuser():
    email = "efpyi@example.com"
    password = "testpass123"
    user = User.objects.create_superuser(
        email=email,
        password=password
    )

    assert user.email == email
    assert user.check_password(password)
    assert user.is_staff
    assert user.is_superuser


@pytest.mark.django_db
def test_check_balance_discount():
    user = User.objects.create_user(
        email="efpyi@example.com",
        password="testtest123"
    )
    user.balance = 10
    assert user.check_balance(5) is None

    with pytest.raises(OperationRateLimitExceeded):
        user.check_balance(11)

    user.discount(5)
    assert user.balance == 5

