import base64
from django.conf import settings
from rest_framework.response import Response
from typing import Literal


def cryption_base64(encrypted_text: str, encode_or_decode: Literal['encode', 'decode'] = 'encode'):
    try:
        converted_2_bytes = encrypted_text.encode("utf-8")
        if encode_or_decode == 'encode':
            return base64.b64encode(converted_2_bytes).decode("utf-8")

        return base64.b64decode(converted_2_bytes).decode("utf-8")

    except Exception as err:
        print(err)


def check_basic_auth(token: str):
    auth = None
    try:
        auth = cryption_base64(token.split(' ')[1], 'decode')
    except Exception:
        pass

    login = 'Paycom'
    passw = 'yfJKzjyPBes#1id6m2r6nsoCSV4cNxUE3bgr'
    hasAuth = auth and len(auth.split(':')) > 1
    req_login = auth.split(':')[0] if hasAuth else None
    req_passw = auth.split(':')[1] if hasAuth else None
    condition = not auth or (token and not auth) or login != req_login or passw != req_passw

    if condition:
        return Response({
            "error": {
                "code": -32504,
                "message": {
                    "ru": "Не авторизован.",
                    "uz": "Avtorizatsiyadan o'tmagan.",
                    "en": "Unauthorized."
                },
                "data": "",
            }
        }, 200)
