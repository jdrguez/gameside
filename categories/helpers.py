from django.http import JsonResponse

from .models import Category


def category_exist(func):
    def wrapper(request, *args, **kwargs):
        try:
            category = Category.objects.get(slug=kwargs['category_slug'])
            request.category = category
            return func(request, *args, **kwargs)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)

    return wrapper
