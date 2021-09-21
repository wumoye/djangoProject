import json
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views import View

from ovaas.models import User
from utils.token_and_session import generate_jwt_token, get_response_json_dict


class PasswordAuthentication(View):

    def get(self, request):
        #
        username = 'lee'
        password = '111'

        user_in_database = User.objects.filter(username=username).exists()
        if not user_in_database:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return JsonResponse(get_response_json_dict(token='ok', state=200, message="ok"))
        else:
            print(f'user exists')

            return JsonResponse(get_response_json_dict(token='exists', state=504, message="exists"))
        #
        # user = authenticate(request, username=username, password=password)
        #
        # if user is not None:
        #
        #         login(request, user)
        #         token = generate_jwt_token(user.username)
        #         return JsonResponse(get_response_json_dict(token=token))
        #
        # else:
        #     return JsonResponse(
        #         get_response_json_dict(token='', state=504, message="Invalid username or password"))


    def post(self, request):
        received_data = json.loads(request.body.decode('utf-8'))
        username = received_data['user']
        password = received_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            token = generate_jwt_token(user.username)

            return JsonResponse(get_response_json_dict(token=token))

        else:
            return JsonResponse(
                get_response_json_dict(token='', state=504, message="Invalid username or password"))
