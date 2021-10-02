import jwt
from django.conf import settings
from django_redis import get_redis_connection


def decrypt(token):
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


def get_username(token):
    dic_data = decrypt(token)
    username = dic_data['username']
    return username


# def set_token_in_redis(key, val, time_out=60 * 60 * 24):
#     con = get_redis_connection('session')
#     res = con.set(key, val, time_out)
#
#     return res
#
#
# def check_token(token):
#     con = get_redis_connection('session')
#     username = get_username(token)
#     last_token = con.get(username)
#     if last_token:
#         return last_token == token
#     return False
