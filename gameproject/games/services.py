from django.db.models import F
from .models import *
from accounts.models import CustomUser


def find_user(username):
    return CustomUser.objects.filter(username=username)


def find_game_creator(game_id):
    game_creator = Game.objects.values_list('creator').get(id=game_id)[0]
    game_creator_user = CustomUser.objects.filter(id=game_creator)
    return game_creator_user


def find_game_price(game_id):
    game_price = Game.objects.values_list('price').get(id=game_id)
    return game_price[0]


def game_purchase(user, game_price, game_creator):
    user.update(balance=F('balance') - game_price)
    game_creator.update(balance=F('balance') + game_price)
