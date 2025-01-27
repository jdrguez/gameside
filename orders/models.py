import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.


class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 1
        CONFIRMED = 2
        CANCELLED = 3
        PAID = -1

    status = models.IntegerField(
        choices=Status, default= 1
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = uuid.uuid4
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
