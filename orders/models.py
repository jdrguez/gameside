import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.


class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 0
        CONFIRMED = 1
        CANCELLED = 2
        PAID = 3

    status = models.IntegerField(
        choices=Status,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = uuid.uuid4
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_orders',
        on_delete=models.CASCADE,
    )
    games = models.ManyToManyField('games.Game', related_name='order_games')

    def get_absolute_url(self):
        return reverse('orders:order-detail', kwargs={'order_pk': self.pk})

    def __str__(self):
        return f'Order estado:{self.status}, User: {self.user}'
