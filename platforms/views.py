from django.shortcuts import get_object_or_404

from .models import Platform


def platform_list(request):
    platforms = Platform.objects.all()
    pass


def platform_detail(request, platform_slug):
    platform = get_object_or_404(Platform, slug=platform_slug)
    pass
