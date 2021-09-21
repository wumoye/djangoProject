import jwt
from django.conf import settings


def get_response_json_dict(token='', status_code=200, message="Success"):
    ret = {
        'status_code': status_code,
        'message': message,
        'access_token': token
    }
    return ret


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
