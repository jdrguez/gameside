import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.


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
    price = 0

    def get_absolute_url(self):
        return reverse('orders:order-detail', kwargs={'order_pk': self.pk})

    def __str__(self):
        return f'Order estado:{self.status}, User: {self.user}'

    @property
    def get_price(self):
        self.price = sum([game.price for game in self.games.all()])
