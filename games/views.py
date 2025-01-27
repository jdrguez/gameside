from django.shortcuts import get_object_or_404

from .models import Game, Review
from .serializer import GameSerializer


def game_list(request):
    if category := request.GET.get('category'):
        games = Game.objects.filter(category__slug=category)
    if platform := request.GET.get('platform'):
        games = Game.objects.filter(platforms__slug=platform)
    if len(request.GET.keys()) == 2:
        category = request.GET.get('category')
        platform = request.GET.get('platform')
        games = Game.objects.filter(platforms__slug=platform, category__slug=category)
    else:
        games = Game.objects.all()

    games_json = GameSerializer(games, request=request)
    return games_json.json_response()


def game_detail(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    game_json = GameSerializer(game, request=request)
    return game_json.json_response()


def review_list(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    reviews = game.games_reviews.all()
    pass


def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    pass


def add_review(request, game_slug):
    pass
