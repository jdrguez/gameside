from django.http import JsonResponse

from .models import Order


def order_exist(func):
    def wrapper(request, *args, **kwargs):
        try:
            print(kwargs)
            order = Order.objects.get(pk=kwargs['order_pk'])
            print(order)
            request.order = order
            return func(request, *args, **kwargs)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

    return wrapper
