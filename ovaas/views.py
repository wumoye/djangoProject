import json
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection

from ovaas.models import User
from utils.session_module import set_session, get_session
from utils.token_module import get_response_json_dict, get_data_from_token


class PasswordAuthentication(View):

    def get(self, request):
        username = 'lee'
        password = '111'

        user_in_database = User.objects.filter(username=username).exists()
        if not user_in_database:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return JsonResponse(get_response_json_dict(token='created', status_code=200, message="created"))
        else:
            print(f'user exists')

            return JsonResponse(get_response_json_dict(token='exists', status_code=504, message="exists"))

        # dict = get_data_from_token()
        # username = request.session.get('lee')
        # password = request.session.get('password')

        # res = get_session(username)
        #
        # return JsonResponse(get_response_json_dict(status_code=0, message=res))

    def post(self, request):
        received_data = json.loads(request.body.decode('utf-8'))
        username = received_data['user']
        password = received_data['password']
        token = ''
        # user_in_database = User.objects.filter(username=username).exists()
        # if not user_in_database:
        #     return JsonResponse(get_response_json_dict(token=token, status_code=401, message="User Does not exist"))
        #
        # user = authenticate(request, username=username, password=password)
        #
        # if user is not None:
        #     login(request, user)
        #
        #     token = user.token
        #     val = {'is_login':True,'user': username}
        #         res = set_session(username, val)
        #
        #     return JsonResponse(
        #         get_response_json_dict(token=token, status_code=200, message=f"User exist,session{res}"))
        # else:
        #     return JsonResponse(
        #         get_response_json_dict(token='', status_code=402, message="Invalid username or password"))

        val = {'is_login': 'true', 'user': username}
        res = set_session(username, val)

        return JsonResponse(
            get_response_json_dict(token=token, status_code=200, message=f"User exist.Set session {res}"))
