import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 1, 'Initiated'
        CONFIRMED = 2, 'Confirmed'
        PAID = 3, 'Paid'
        CANCELLED = -1, 'Cancelled'

    status = models.IntegerField(choices=Status, default=Status.INITIATED)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_orders',
        on_delete=models.CASCADE,
    )
    games = models.ManyToManyField('games.Game', related_name='order_games', null=True)

    def get_absolute_url(self):
        return reverse('orders:order-detail', kwargs={'order_pk': self.pk})

    def __str__(self):
        return f'Order estado:{self.status}, User: {self.user}'

    def change_status(self, status: int):
        self.status = status

    def is_initiated(self):
        return self.status == 1

    def num_games_in_order(self):
        return self.games.all().count()

    def add_game(self, game):
        self.games.add(game)
        game.stock -= 1

    @property
    def price(self):
        return sum([game.price for game in self.games.all()])
