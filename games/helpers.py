from django.http import JsonResponse

from .models import Game, Review


def game_exist(func):
    def wrapper(*args, **kwargs):
        try:
            game = Game.objects.get(slug=kwargs['game_slug'])
            args[0].game = game
            return func(*args, **kwargs)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)

    return wrapper


def game_exist_post(func):
    def wrapper(request, *args, **kwargs):
        game_slug = request.json_body['game-slug']
        print(game_slug)
        try:
            game = Game.objects.get(slug=game_slug)
            request.game = game
            return func(request, *args, **kwargs)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)

    return wrapper


def review_exist(func):
    def wrapper(*args, **kwargs):
        try:
            review = Review.objects.get(pk=kwargs['review_pk'])
            args[0].review = review
            return func(*args, **kwargs)
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found'}, status=404)

    return wrapper
