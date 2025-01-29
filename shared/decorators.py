import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse


def auth_required(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        json_post = json.load(request.body)
        user = get_user_model()
        try:
            user = user.objects.get(token__key=json_post['token'])
            request.json_post = json_post
        except user.DoesNotExist:
            return JsonResponse({'error': 'Invalid Token'}, status=401)

    return wrapper


def method_required(method):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method == method.upper():
                return func(request, *args, **kwargs)
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        return wrapper

    return decorator


def user_owner(func):
    def wrapper(request, *args, **kwargs):
        json_post = json.load(request.body)
        print(json_post)
        user = get_user_model()
        user = user.objects.get(token=json_post['key'])
        if user == request.user:
            return func(request, *args, **kwargs)
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

    return wrapper
