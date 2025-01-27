from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import JsonResponse
from .models import Game, Review
from .serializer import GameSerializer

def game_list(request):
    games = Game.objects.all()
    games_json = GameSerializer(games, request=request)
    return games_json.json_response()


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
