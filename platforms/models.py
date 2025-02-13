from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Platform(models.Model):
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logos', default='logos/default.jpg')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('platforms:platform-detail', kwargs={'platform_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
