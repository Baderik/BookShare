from django.urls import path
from authentication.views import IndexView, LoginView, SignUpView, LogoutView

urlpatterns = [
    path("", IndexView.as_view()),
    path("login/", LoginView.as_view()),
    path("registration/", SignUpView.as_view()),
    path("logout/", LogoutView.as_view()),
]
