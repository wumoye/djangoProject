import jwt
from datetime import datetime, timedelta

from django.conf import settings


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