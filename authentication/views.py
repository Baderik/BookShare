from django.shortcuts import render, redirect
from django.views import View
# Create your views here.


class IndexView(View):
    @staticmethod
    def get(request):
        return redirect("login/")


class LoginView(View):
    @staticmethod
    def get(request):
        return render(request, "auth/login.html")


class SignUpView(View):
    @staticmethod
    def get(request):
        return render(request, "auth/register.html")
