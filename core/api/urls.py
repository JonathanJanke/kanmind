from django.urls import path
from authentication_app.views import UserLoginView, UserRegistrationView
from boards_app.views import BoardListView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('boards/', BoardListView.as_view(), name='board-list'),
]