from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Game, Review


def game_list(request, filter=''):
    if filter:
        games = Game.objects.filter(name=filter)
    games = get_list_or_404(Game)
    pass


def game_detail(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    pass


def review_list(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    reviews = game.games_reviews.all()
    pass


def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    pass


def add_review(request, game_slug):
    pass
