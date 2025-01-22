from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.text.utils import slugify
from django.urls import reverse

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
        min_value=0,
        max_digits=6,
        decimal_places=2,
    )
    stock = models.IntegerField()
    released_at = models.DateField()
    pegi = models.IntegerField(
        choices=Pegi,
        max_length=1,
    )
    category = models.ForeignKey(
        'categories.Category',
        related_name='game_categories',
        on_delete=models.SET_NULL,
    )
    platforms = models.ManyToManyField(
        'platforms.Platform', related_name='game_platforms', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Nombre: {self.title}, Categoria: {self.category}, Plataforma: {self.platforms}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Review(models.Model):
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        MinValueValidator(limit_value=0), MaxValueValidator(limit_value=5)
    )
    game = models.ForeignKey(Game, related_name='reviews', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('_detail', kwargs={'pk': self.pk})
