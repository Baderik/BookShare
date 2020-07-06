from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from authentication.forms import LoginForm, RegisterForm
from authentication.models import User
from authentication.tokens import account_activation_token
import BookShare.settings as settings


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
        user = User.objects.filter(email=email).count()

        if user:
            result["code"] = "400"
            result["message"] = "Пользователь с такой почтой уже существует"

        else:
            user = User(email=email)
            # user.token = token
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            token = account_activation_token.make_token(user)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            url = f"https://{settings.ALLOWED_HOSTS[-1]}" \
                  f"/auth/activation/{uid}/{token}"
            send_mail(
                subject="Активация аккаунта | Book.Share",
                message="",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=get_template(
                    "letterActivation.html").render(
                    {"password": password, "url": url,
                     "host": settings.ALLOWED_HOSTS[-1],
                     "logo": "static/img/logo.png"})
            )

            print(f"Activate url: {url}\nPassword: {password}")

            result["code"] = "200"
            result["message"] = \
                "На вашу почту отправленно сообщение с инстукцией."

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
            result["message"] = \
                "Проверьте правильно ли вы заполнили поля"
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


class ActivationView(View):
    @staticmethod
    def get(request, uid, token):
        try:
            decode_uid = force_text(urlsafe_base64_decode(uid))

        except (TypeError, ValueError, OverflowError):
            print("decode")
            return redirect('/')

        user = get_object_or_404(User, pk=decode_uid)

        if account_activation_token.check_token(user, token) and \
                not user.is_active_email:
            return render(request, 'auth/activation.html',
                          {"form_in": LoginForm(),
                           "user": request.user})

        return redirect('/')

    @staticmethod
    def post(request, uid, token):
        if request.user.is_authenticated:
            return redirect("/")

        form = LoginForm(request.POST)

        if not form.is_valid():
            return JsonResponse({
                "code": "400",
                "message": "Проверьте правильно ли вы заполнили поля"})

        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        try:
            uid = force_text(urlsafe_base64_decode(uid))

        except (TypeError, ValueError, OverflowError):
            return redirect("/")

        user = get_object_or_404(User, pk=uid)

        if not account_activation_token.check_token(user, token) or\
                user.is_active_email:
            return redirect("/")

        user = authenticate(email=email, password=password)

        if user is None:
            return JsonResponse({
                "code": "401",
                "message":
                    "Пользователь c такой почтой и паролем не найден"})

        user.is_active_email = True
        user.save()
        login(request, user)

        return redirect("/")
