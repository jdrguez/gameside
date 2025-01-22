from django.shortcuts import get_object_or_404

from .models import Category


def category_list(request):
    categories = Category.objects.all()
    pass


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    pass
