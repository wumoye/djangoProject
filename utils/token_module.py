import jwt
import json
from django.conf import settings
from django_redis import get_redis_connection
from datetime import datetime, timedelta


def get_data_from_token(token):
    ret = {
        'username': '',
        'message': 'Success',
        'status_code': -1
    }
    try:
        dict_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        ret['status_code'] = 200
        ret['username'] = dict_data.get('data').get('username')
    except jwt.ExpiredSignatureError:
        ret['status_code'] = 411
        ret['message'] = 'Token expired'
    except jwt.InvalidTokenError:
        ret['status_code'] = 412
        ret['message'] = 'Invalid token'
    except Exception as e:
        ret['status_code'] = 413
        ret['message'] = 'Can not get user object'

    return ret


def set_token_in_redis(key, val):
    con = get_redis_connection('session')
    res = con.set(key, val, 60 * 60 * 24)

    return res


def check_token_in_redis(key):
    con = get_redis_connection('session')
    val = con.get(key)
    if not val:
        return None
    else:
        return val.decode("utf-8")
