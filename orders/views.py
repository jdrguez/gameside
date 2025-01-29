from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import (
    check_json_body,
    method_required,
    required_fields,
    user_owner,
    valid_token,
)

from .helpers import order_exist
from .models import Order
from .serializer import OrderSerializer


@method_required('post')
@check_json_body
@required_fields('token')
@valid_token
@csrf_exempt
def add_order(request):
    user = User.objects.get(token=request.token)
    order = Order.objects.create(user=user)
    order_json = OrderSerializer(order, request=request)
    return order_json.json_response()


@method_required('post')
@check_json_body
@required_fields('token')
@valid_token
@order_exist
@csrf_exempt
@user_owner
def order_detail(request, order_pk):
    order_json = OrderSerializer(request.order, request=request)
    return order_json.json_response()


def confirm_order(request, order_pk):
    pass


def cancel_order(request, order_pk):
    pass


def pay_order(request, order_pk):
    pass
