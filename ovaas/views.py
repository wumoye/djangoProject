import json
from django.contrib.auth import login, authenticate, logout
from django.db import models
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection

from ovaas.models import User
from utils.token_module import *


class PasswordAuthentication(View):

    def get(self, request):
        # test code----start
        # username = 'lee2'
        # password = '111'
        #
        # user_in_database = User.objects.filter(username=username).exists()
        # if not user_in_database:
        #     user = User.objects.create_user(username=username, password=password)
        #     user.save()
        #     return JsonResponse(get_response_json_dict(token='created', status_code=200, message="created"))
        # else:
        #     print(f'user exists')
        #
        #     return JsonResponse(get_response_json_dict(token='exists', status_code=504, message="exists"))

        # dict = get_data_from_token()
        # username = request.session.get('lee')
        # password = request.session.get('password')
        # token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzI3NTYwMjIsImlhdCI6MTYzMjY2OTYyMiwiZGF0YSI6eyJ1c2VybmFtZSI6ImxlZTIifX0.KKywrzGhmJCQ7On3sl6w5vzQVlaF7rqzx-FCClmHApw'
        # token_false = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzI3NTYwMjIsImlhdCI6MTYzMjY2OTYyMiwiZGF0YSI6eyJ1c1VybmFtZSI6ImxlZTIifX0.KKywrzGhmJCQ7On3sl6w5vzQVlaF7rqzx-FCClmHApw'
        # token = token_false
        # res = check_token_in_redis(token)
        # message = f"res: {res}."
        # status_code = 200
        # if not res:
        #     message += "Invalid token"
        #     status_code = 412
        # else:
        #     data = get_data_from_token(token)
        #     if data['username'] == res:
        #         message += f"The token is user. username:{data}"
        #     else:
        #         message += f"Invalid token. username:{data}"
        #         status_code = 412
        # #
        # return JsonResponse(get_response_json_dict(token, status_code=status_code, message=message))
        # test code----end

        # sessions = request.session.get('user', "")
        # return JsonResponse({'session': sessions})
        pass

    def post(self, request):
        received_data = json.loads(request.body.decode('utf-8'))
        username = received_data['user']
        password = received_data['password']
        token = ''
        user_in_database = User.objects.filter(username=username).exists()
        if not user_in_database:
            return JsonResponse({'401': 'User Does not exist'})

        user = authenticate(request, username=username, password=password)

        if user is not None:

            token = user.token
            request.session['user'] = token
            login(request, user)
            # session_id = request.session.get('user', '')

            # res = set_token_in_redis(token, username)
            # res = None
            return JsonResponse({'access_token': token})
        else:
            return JsonResponse({'402': 'Invalid username or password'})

        # test code----start
        # val = {'is_login': 'true', 'user': username}
        # res = set_session(username, val)
        #
        # return JsonResponse(
        #     get_response_json_dict(token=token, status_code=200, message=f"User exist.Set session {res}"))
        # test code----end