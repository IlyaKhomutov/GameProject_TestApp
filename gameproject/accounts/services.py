from django.db.models import F

from .models import *


def find_user(username):
    return CustomUser.objects.filter(username=username)


def do_deposit(user, amount):
    user.update(balance=F('balance') + amount)


def find_deposit(deposit_id):
    return Deposit.objects.filter(id=deposit_id)


def rollback(user, deposit, deposit_amount):
    deposit.update(status='cancelled')
    user.update(balance=F('balance') - deposit_amount)
