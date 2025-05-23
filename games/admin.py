from django.contrib import admin

from .models import Game, Review


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'cover',
        'price',
        'stock',
        'released_at',
        'pegi',
        'category',
    ]
    filter_horizontal = ('platforms',)
    prepopulated_fields = {'slug': ['title']}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'rating',
        'comment',
        'game',
        'author',
        'created_at', 
        'updated_at',
    ]
