from django.urls import path
from authentication.views import IndexView, LoginView, SignUpView

urlpatterns = [
    path("", IndexView.as_view()),
    path("login/", LoginView.as_view()),
    path("register/", SignUpView.as_view())
]
