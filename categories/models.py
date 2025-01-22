from colorfield.fields import ColorField
from django.db import models
from django.text.utils import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = ColorField()

    def __str__(self):
        return f'Categoria con nombre: {self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
