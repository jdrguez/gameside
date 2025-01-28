from shared.decorators import method_required

from .helpers import category_exist
from .models import Category
from .serializer import CategorySerializer


@method_required('get')
def category_list(request):
    categories = Category.objects.all()
    categories_json = CategorySerializer(categories, request=request)
    return categories_json.json_response()


@method_required('get')
@category_exist
def category_detail(request, category_slug):
    category_json = CategorySerializer(request.category, request=request)

    return category_json.json_response()
