from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

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
    cover = models.ImageField(upload_to='covers', default='covers/default.jpg')
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
    
    def update_stock(self, num, action):
        match action:
            case 'add':
                self.stock += num
            case 'remove':
                self.stock += num

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('games:game-detail', kwargs={'game_slug': self.slug})


class Review(models.Model):
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=5),
        ]
    )
    game = models.ForeignKey(Game, related_name='game_reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_reviews',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('games:review-detail', kwargs={'review_pk': self.pk})
