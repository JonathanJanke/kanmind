from django.urls import path
from authentication_app.views import UserLoginView, UserRegistrationView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]