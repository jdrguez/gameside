from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.helpers import game_exist
from games.serializer import GameSerializer
from shared.decorators import (
    check_json_body,
    method_required,
    required_fields,
    user_owner,
    valid_token,
)

from .helpers import order_exist, status_errors, validate_card
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
def order_game_list(request, order_pk):
    game_json = GameSerializer(request.order.games.all(), request=request)
    return game_json.json_response()


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


@method_required('post')
@check_json_body
@required_fields('token')
@valid_token
@order_exist
@csrf_exempt
@user_owner
@status_errors('confirmed')
def confirm_order(request, order_pk):
    order = request.order
    order.change_status(2)
    return JsonResponse({'status': order.get_status_display()})


@method_required('post')
@check_json_body
@required_fields('token')
@valid_token
@order_exist
@csrf_exempt
@user_owner
@status_errors('cancelled')
def cancel_order(request, order_pk):
    order = request.order
    order.change_status(-1)
    return JsonResponse({'status': order.get_status_display()})


@method_required('post')
@check_json_body
@required_fields('token', 'card-number', 'exp-date', 'cvc')
@valid_token
@order_exist
@csrf_exempt
@user_owner
@status_errors('paid')
@validate_card
def pay_order(request, order_pk):
    order = request.order
    order.change_status(3)
    return JsonResponse({'status': order.get_status_display()})


@method_required('post')
@check_json_body
@required_fields('token')
@valid_token
@order_exist
@game_exist
@csrf_exempt
@user_owner
def add_game_to_order(request, order_pk, game_slug):
    order = request.order
    game = request.game
    order.add_game(game)
    return JsonResponse({'num-games-in-order': order.num_games_in_order()})
