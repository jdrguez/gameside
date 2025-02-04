import json
import re
from json.decoder import JSONDecodeError

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse

from orders.models import Order
from users.models import Token

from .helpers import get_token

""" 
def auth_required(func):
    def wrapper(request, *args, **kwargs):
        json_post = json.loads(request.body)
        print(json_post)
        user = get_user_model()
        try:
            user = user.objects.get(token__key=json_post['token'])
            request.json_post = json_post
            return func(request, *args, **kwargs)
        except user.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)

    return wrapper """


def auth_required(func):
    def wrapper(request, *args, **kwargs):
        if user := authenticate(
            username=request.json_body['username'], password=request.json_body['password']
        ):
            request.user = user
            return func(request, *args, **kwargs)
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return wrapper


def token_exists(func):
    def wrapper(request, *args, **kwargs):
        auth = request.headers.get('Authoritation', 'no existe')
        try:
            if auth_value := get_token(auth):
                Token.objects.get(key=auth_value)
                request.user = User.objects.get(token__key=auth_value)
                return func(request, *args, **kwargs)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

    return wrapper


def valid_token(func):
    def wrapper(request, *args, **kwargs):
        auth = request.headers.get('Authorization', 'no existe')
        regexp = 'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
        if auth_value := re.fullmatch(regexp, auth):
            request.user = User.objects.get(token__key=auth_value)
            return func(request, *args, **kwargs)
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    return wrapper


def method_required(method):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method == method.upper():
                return func(request, *args, **kwargs)
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        return wrapper

    return decorator


def check_json_body(func):
    def wrapper(request, *args, **kwargs):
        try:
            json_body = json.loads(request.body)
            request.json_body = json_body
            return func(request, *args, **kwargs)
        except JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    return wrapper


def user_owner(func):
    def wrapper(request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['order_pk'])
        user = request.user
        if order.user == user:
            return func(request, *args, **kwargs)
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

    return wrapper


def required_fields(*fields):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            json_body = json.loads(request.body)
            for field in fields:
                if field not in json_body:
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
