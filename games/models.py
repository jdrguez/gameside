from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Game(models.Model):
    class Pegi(models.IntegerChoices):
        PEGI3 = 3
        PEGI7 = 7
        PEGI12 = 12
        PEGI16 = 16
        PEGI18 = 18

    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='covers', default='covers/nocover.png')
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    stock = models.IntegerField()
    released_at = models.DateField()
    pegi = models.IntegerField(
        choices=Pegi,
    )
    category = models.ForeignKey(
        'categories.Category',
        related_name='game_categories',
        on_delete=models.SET_NULL,
        null=True,
    )
    platforms = models.ManyToManyField(
        'platforms.Platform',
        related_name='game_platforms',
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('games:game-detail', kwargs={'game_slug': self.slug})


class Review(models.Model):
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(limit_value=0), MaxValueValidator(limit_value=5)]
    )
    game = models.ForeignKey(Game, related_name='game_reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_reviews',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('games:review-detail', kwargs={'review_pk': self.pk})
