from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import View

import re

from ovaas.models import User
from utils.mixin import LoginRequiredMixin


class RegisterView(View):
    """Register"""

    def get(self, request):
        """Register page"""

        return render(request, 'regester.html')

    def post(self, request):
        """Registration processing"""
        # Accept data
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        passwordc = request.POST.get('cpwd')
        email = request.POST.get('email')

        if not all([username, password, email]):
            # Incomplete data
            return render(request, 'regester.html', {'errmsg': 'Incomplete data'})
            # Check mail
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'regester.html', {'errmsg': 'The mail format is incorrect'})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # user name does not exist
            user = None
        if user:
            return render(request, 'index.html', {'errmsg': 'User name already exists'})

        if passwordc != password:
            return render(request, 'regester.html', {'errmsg': 'Inconsistent passwords'})

        # processing
        user = User.objects.create_user(username, email, password)
        user.is_active = 1
        user.save()
        login(request, user)
        return render(request, 'index.html', {'username': username})


# /user/login
class LoginView(View):
    """login"""

    def get(self, request):
        """Login page"""
        # return redirect(reverse('ovaas:index'))
        return render(request, 'index.html')

    def post(self, request):
        """Login verification"""

        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # Data verification
        if not all([username, password]):
            return render(request, 'index.html', {'errmsg': 'データが不完全'})
        print(username, password)

        # processing: Registration check
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # the password verified for the user
            if user.is_active:

                login(request, user)

                next_url = request.GET.get('next', reverse('ovaas:index'))

                # Go to top page
                response = redirect(next_url)  # HttpResponseRedirect

                return response
            else:
                print(f"user.is_active is false")
                # User not activated
                return render(request, 'index.html', {'errmsg': 'The user is not active'})

        else:
            # Username or password is wrong
            return render(request, 'index.html', {'errmsg': 'Username or password is wrong'})


# /user/logout
class LogoutView(View):
    """logout"""

    def get(self, request):
        """logout"""
        # Delete session
        logout(request)

        # Go to top page
        return redirect(reverse('ovaas:index'))


class ShowView(LoginRequiredMixin, View):
    def get(self, request):
        users_data = User.objects.filter()

        username = request.user

        return render(request, 'index.html', {'users_data': users_data, 'username': username})

    def post(self, request):
        pass
