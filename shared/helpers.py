import re


def get_token(value: str):
    regexp = 'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    if auth_value := re.fullmatch(regexp, value):
        return auth_value['token']
    return False
