from django.http import JsonResponse

from shared.decorators import auth_required, check_json_body, method_required, required_fields


@method_required('post')
@check_json_body
@required_fields('username', 'password')
@auth_required
def auth(request):
    print(request.user)
    return JsonResponse({'token': request.user.token.key})
