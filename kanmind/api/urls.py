from django.contrib import admin
from django.urls import include, path
from .views import UserLoginView, UserRegistrationView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]