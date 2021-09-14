from django.urls import path, include
from ovaas.views import PasswordAuthentication

urlpatterns = [
    path('api/v1/auth', PasswordAuthentication.as_view(), name='auth'),
]
