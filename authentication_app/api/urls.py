from django.urls import path
from authentication_app.views import UserLoginView, UserRegistrationView, email_check

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path("email-check/<str:email>/", email_check, name="user-email-check")
]