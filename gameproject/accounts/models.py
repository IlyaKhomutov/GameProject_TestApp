import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    balance = models.IntegerField("Balance", help_text="Balance in cents", default=0)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username}"


class Deposit(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='username', related_name='deposits',
                             help_text="Unique username")
    amount = models.IntegerField("Amount", help_text="In cents")
    status = models.CharField("Status", default="success", max_length=100)

    class Meta:
        verbose_name = "Deposit"
        verbose_name_plural = "Deposits"

    def __str__(self):
        return f"Deposit {self.id}"
