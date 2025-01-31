from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import (
    check_json_body,
    method_required,
    required_fields,
    valid_token,
)

from .helpers import game_exist, review_exist
from .models import Game, Review
from .serializer import GameSerializer, ReviewSerializer


@method_required('get')
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


@method_required('get')
@game_exist
def game_detail(request, game_slug):
    game_json = GameSerializer(request.game, request=request)
    return game_json.json_response()


@method_required('get')
@game_exist
def review_list(request, game_slug):
    reviews = request.game.game_reviews.all()
    review_json = ReviewSerializer(reviews, request=request)
    return review_json.json_response()


@method_required('get')
@review_exist
def review_detail(request, review_pk):
    review_json = ReviewSerializer(request.review, request=request)
    return review_json.json_response()


@csrf_exempt
@method_required('post')
@check_json_body
@required_fields('token', 'rating', 'comment')
@valid_token
@game_exist
def add_review(request, game_slug):
    user = User.objects.get(token=request.token)
    rating = int(request.json_body['rating'])
    if rating < 1 or rating > 5:
        return JsonResponse({'error': 'Rating is out of range'}, status=400)
    review = Review.objects.create(
        game=request.game,
        author=user,
        rating=rating,
        comment=request.json_body['comment'],
    )
    return JsonResponse({'id': review.pk})
