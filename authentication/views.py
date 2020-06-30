from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from authentication.forms import LoginForm, RegisterForm
from authentication.models import User


class IndexView(View):
    @staticmethod
    def get(request):
        return redirect("login/")

    @staticmethod
    def post(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")

        result = {"code": "500", "message": "Произошла ошибка"}

        form = RegisterForm(request.POST)

        if not form.is_valid():
            result["code"] = "400"
            result["message"] = "Проверьте правильно ли вы заполнили поля"

            for field in ("email",):
                result[field] = "1" \
                    if form.cleaned_data.get(field, "") \
                    else ""

            return JsonResponse(result)

        email = form.cleaned_data.get("email", "")
        user = User.objects.get(email=email)

        if user is not None:
            result["code"] = "400"
            result["message"] = "Пользователь с такой почтой уже существует"

        else:
            user = User(email=email)

            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()

            print(f"Password: {password}")

            result["code"] = "200"
            result["message"] = "На вашу почту отправленно сообщение с инстукцией."

        return JsonResponse(result)


class LoginView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect("/")

        return render(request, "auth/login.html", {
            "form": LoginForm(),
            "user": request.user
        })

    @staticmethod
    def post(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")

        result = {"code": "500", "message": "Произошла ошибка"}
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active_email:
                    login(request, user)

                    url = "/people/settings/"

                    if user.is_active:
                        url = "/"

                    result["code"] = "303"
                    result["message"] = "Вам туда"
                    result["location"] = url

                else:
                    result["code"] = "401"
                    result["message"] = "Сначала подтвердите почту"

            else:
                result["code"] = "401"
                result["message"] = "Пользователь c такой почтой" \
                                    " и паролем не найден"

        else:
            result["code"] = "400"
            result["message"] = "Проверьте правильно ли вы заполнили поля"
            for field in ("email", "password"):
                result[field] = "1" \
                    if form.cleaned_data.get(field, "") \
                    else ""

        return JsonResponse(result)


class SignUpView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect("/")

        return render(request, "auth/register.html", {
            "form": RegisterForm(),
            "user": request.user
        })


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect("/")
