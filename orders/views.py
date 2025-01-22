from django.shortcuts import get_object_or_404

from .models import Order


# Create your views here.
def add_order(request):
    pass


def order_detail(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    pass


def confirm_order(request, order_pk):
    pass


def cancel_order(request, order_pk):
    pass


def pay_order(request, order_pk):
    pass
