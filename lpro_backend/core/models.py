from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from calculator.exceptions import OperationRateLimitExceeded


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users must require an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField("Email address", unique=True)
    balance = models.DecimalField(default=0, max_digits=7, decimal_places=3)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def check_balance(self, amount):
        if self.balance < amount:
            raise OperationRateLimitExceeded("The user has insufficient balance.")

    def discount(self, amount):
        if self.balance < amount:
            raise OperationRateLimitExceeded("The user has insufficient balance.")
        self.balance -= amount
        self.save()


