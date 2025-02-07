from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.helpers import game_exist_post
from games.serializer import GameSerializer
from shared.decorators import (
    check_json_body,
    method_required,
    required_fields,
    token_exists,
    user_owner,
    valid_token,
)

from .helpers import order_exist, status_errors, valid_status, validate_card
from .models import Order
from .serializer import OrderSerializer


@method_required('post')
@check_json_body
@valid_token
@token_exists
@csrf_exempt
def add_order(request):
    user = request.user
    order = Order.objects.create(user=user)
    order_json = OrderSerializer(order, request=request)
    return order_json.json_response()


@csrf_exempt
@method_required('get')
@valid_token
@token_exists
@order_exist
@user_owner
def order_game_list(request, order_pk):
    game_json = GameSerializer(request.order.games.all(), request=request)
    return game_json.json_response()


@csrf_exempt
@method_required('get')
@valid_token
@token_exists
@order_exist
@user_owner
def order_detail(request, order_pk):
    order_json = OrderSerializer(request.order, request=request)
    return order_json.json_response()


""" 
@method_required('post')
@check_json_body
@valid_token
@token_exists
@order_exist
@csrf_exempt
@user_owner
@status_errors('confirmed')
def confirm_order(request, order_pk):
    order = request.order
    order.change_status(2)
    order.save()
    return JsonResponse({'status': order.get_status_display()})


@method_required('post')
@check_json_body
@valid_token
@token_exists
@order_exist
@csrf_exempt
@user_owner
@status_errors('cancelled')
def cancel_order(request, order_pk):
    order = request.order
    order.change_status(-1)
    order.save()
    for game in order.games.all():
        game.update_stock(1, 'add')
        game.save()
    return JsonResponse({'status': order.get_status_display()})
 """


@method_required('post')
@check_json_body
@required_fields('status')
@valid_token
@token_exists
@order_exist
@user_owner
@valid_status
@status_errors('cancelled')
def change_order_status(request, order_pk):
    order = request.order
    order.change_status(request.status)
    order.save()
    return JsonResponse({'status': order.get_status_display()})


@method_required('post')
@check_json_body
@required_fields('card-number', 'exp-date', 'cvc')
@valid_token
@token_exists
@order_exist
@csrf_exempt
@user_owner
@status_errors('paid')
@validate_card
def pay_order(request, order_pk):
    order = request.order
    order.change_status(3)
    order.save()
    return JsonResponse({'status': order.get_status_display()})


@csrf_exempt
@method_required('post')
@check_json_body
@required_fields('game-slug')
@valid_token
@token_exists
@order_exist
@game_exist_post
@user_owner
def add_game_to_order(request, order_pk):
    order = request.order
    order.add_game(request.game)
    return JsonResponse({'num-games-in-order': order.num_games_in_order()})
