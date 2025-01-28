from shared.decorators import method_required

from .helpers import platform_exist
from .models import Platform
from .serializer import PlatformSerializer


@method_required('get')
def platform_list(request):
    platforms = Platform.objects.all()
    platforms_json = PlatformSerializer(platforms, request=request)
    return platforms_json.json_response()


@method_required('get')
@platform_exist
def platform_detail(request, platform_slug):
    platform_json = PlatformSerializer(request.platform, request=request)
    return platform_json.json_response()
