from shared.decorators import method_required

from .helpers import order_exist
from .serializer import OrderSerializer


# Create your views here.
def add_order(request):
    pass


@method_required('get')
@order_exist
def order_detail(request, order_pk):
    order_json = OrderSerializer(request.order, request=request)
    return order_json.json_response()


def confirm_order(request, order_pk):
    pass


def cancel_order(request, order_pk):
    pass


def pay_order(request, order_pk):
    pass
