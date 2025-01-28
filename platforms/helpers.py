from django.http import JsonResponse

from .models import Platform


def platform_exist(func):
    def wrapper(request, *args, **kwargs):
        try:
            platform = Platform.objects.get(slug=kwargs['platform_slug'])
            request.platform = platform
            return func(request, *args, **kwargs)
        except Platform.DoesNotExist:
            return JsonResponse({'error': 'Platform not found'}, status=404)

    return wrapper
