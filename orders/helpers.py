import re
from datetime import datetime

from django.http import JsonResponse

from .models import Order


def order_exist(func):
    def wrapper(request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs['order_pk'])
            request.order = order
            return func(request, *args, **kwargs)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

    return wrapper


def regex_validator(key: str, regex: str, request) -> bool:
    return re.match(regex, request.json_body[key]) is None


def validate_card(func):
    def wrapper(request, *args, **kwargs):
        regex_num_card = r'^[0-9]{4}(-[0-9]{4}){3}$'
        regex_exp_date = r'^(0[1-9]|1[0-2])/\d{4}$'
        regex_cvc = r'^\d{3}$'

        error = None
        if regex_validator(key='card-number', regex=regex_num_card, request=request):
            error = 'Invalid card number'
        if regex_validator(key='exp-date', regex=regex_exp_date, request=request):
            error = 'Invalid expiration date'
        if regex_validator(key='cvc', regex=regex_cvc, request=request):
            error = 'Invalid CVC'
        try:
            card_date = datetime.strptime(request.json_body['exp-date'] , '%m/%Y')
            current_date = datetime.now()
            if current_date >= card_date:
                error = 'Card expired'
        except ValueError:
            None

        if error:
            return JsonResponse({'error': f'{error}'}, status=400)

        return func(request, *args, **kwargs)

    return wrapper


def status_errors(status):
    status = status.upper()

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            order = request.order
            match status:
                case 'CONFIRMED':
                    if order.is_initiated():
                        return func(request, *args, **kwargs)
                    return JsonResponse(
                        {'error': 'Orders can only be confirmed when initiated'}, status=400
                    )
                case 'CANCELLED':
                    if order.is_initiated():
                        return func(request, *args, **kwargs)
                    return JsonResponse(
                        {'error': 'Orders can only be cancelled when initiated'}, status=400
                    )
                case 'PAID':
                    if order.status == 2:
                        return func(request, *args, **kwargs)
                    return JsonResponse(
                        {'error': 'Orders can only be payed when confirmed'}, status=400
                    )

        return wrapper

    return decorator
