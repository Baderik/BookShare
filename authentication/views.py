from django.shortcuts import render, redirect
from django.views import View

from authentication.forms import LoginForm, RegisterForm


class IndexView(View):
    @staticmethod
    def get(request):
        return redirect("login/")


class LoginView(View):
    @staticmethod
    def get(request):
        return render(request, "auth/login.html", {"form": LoginForm()})


class SignUpView(View):
    @staticmethod
    def get(request):
        return render(request, "auth/register.html", {"form": RegisterForm()})
