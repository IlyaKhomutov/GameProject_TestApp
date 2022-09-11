import uuid
from django.db import models
from accounts.models import CustomUser


class Game(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    title = models.CharField("Title", max_length=150, help_text="Full name of the game")
    price = models.IntegerField("Price", help_text="In cents")
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='creator',
                                related_name='created_games')

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"

    def __str__(self):
        return f'{self.title}'


class Purchase(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='user', related_name='purchases')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='game', related_name='purchases')

    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"

    def __str__(self):
        return f" Purchase {self.id}"
