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
            request.session['user'] = user.username
            request.session['token'] = token
            # key=request.session.session_key
            login(request, user)
            # session_id = request.session.get('user', '')

            return JsonResponse({'access_token': token})
        else:
            return JsonResponse({'402': 'Invalid username or password'})
