import json
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import login, authenticate

from django.http import JsonResponse
from django.views import View
import jwt


def generate_jwt_token(username):
    token = jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'data': {
            'username': username
        }
    }, settings.SECRET_KEY, algorithm='HS256')

    return token.encode('utf-8').decode('utf-8')


def get_response_json_dict(token, state=200, message="Success"):
    ret = {
        'state': state,
        'message': message,
        'access_token': token
    }
    return ret


class PasswordAuthentication(View):

    def get(self, request):
        pass

    def post(self, request):
        received_data = json.loads(request.body.decode('utf-8'))
        username = 'Ouchiyama'
        password = received_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                token = generate_jwt_token(user.username)
                return JsonResponse(get_response_json_dict(token=token))
            else:
                return JsonResponse(
                    get_response_json_dict(token='', state=-1, message="User not activated"))
        else:
            return JsonResponse(
                get_response_json_dict(token='', state=-1, message="Invalid username or password"))
