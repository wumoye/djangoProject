from django.urls import path, include
from ovaas.views import LoginView

urlpatterns = [
    path('api/v1/auth', LoginView.as_view(), name='auth'),
]
