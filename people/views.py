from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View

from re import match

from authentication.tokens import account_activation_token
import BookShare.settings as settings
from imageBase.forms import UploadImageForm
from people.forms import SettingsForm


class IndexView(View):
    @staticmethod
    def get(request):
        return redirect("1/")


class ProfileView(View):
    @staticmethod
    def get(request, uid):
        user = get_object_or_404(get_user_model(), id=uid)

        return render(request, "people/profile.html", {
            "user": request.user,
            "owner": user,
            "is_owner": request.user.id == user.id,
            "articles": user.article_set.order_by("-date")
        })

    @staticmethod
    def post(request, uid, *args, **kwargs):
        if not request.user.is_authenticated or uid != request.user.pk:
            return JsonResponse({"code": "403", "message": "Вам туда нельзя"})

        form = SettingsForm(request.POST, instance=request.user.profile)

        if not form.is_valid() or \
                not check_phone(form.cleaned_data["phone"]):
            return JsonResponse({
                "code": "400",
                "message": "Проверьте правильно ли вы заполнили поля"})

        message = []

        if request.user.email != form.cleaned_data["email"]:
            if get_user_model().objects.filter(
                    email=form.cleaned_data["email"]):
                return JsonResponse({
                    "code": "400",
                    "message": "Эту почту уже кто-то использует"})

            request.user.email = form.cleaned_data["email"]
            request.user.is_active_email = False
            token = account_activation_token.make_token(request.user)
            uid = urlsafe_base64_encode(force_bytes(request.user.pk))
            url = f"https://{settings.ALLOWED_HOSTS[-1]}" \
                  f"/auth/activation/{uid}/{token}"
            send_mail(
                subject="Активация аккаунта | Book.Share",
                message="",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                html_message=get_template(
                    "letterActivation.html").render(
                    {"password": "Пароль остался старый",
                     "url": url,
                     "host": settings.ALLOWED_HOSTS[-1],
                     "logo": "static/img/logo.png"})
            )

            print(f"Activate url: {url}")
            message.append("Ваша почта изменена")

        if form.cleaned_data["password"]:
            if form.cleaned_data["password"] \
                    == form.cleaned_data["password_again"]:
                message.append("Ваш пароль изменён")

            else:
                return JsonResponse({"code": "400",
                                     "message": "Пароли не совпадают"})

        request.user.is_active = True
        request.user.save()

        if not message:
            message = ["Сохранено"]

        return JsonResponse({"code": "200",
                             "message": "\n".join(message),
                             "email": request.user.is_active_email})


class SettingsView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return render(request, "people/settings.html",
                          {"form": SettingsForm(
                              instance=request.user.profile,
                              initial={
                                  "email": request.user.email
                              }
                          ),
                              "email": request.user.is_active_email,
                              "user": request.user,
                              "imageForm": UploadImageForm
                          })

        return redirect("/")


def check_phone(phone):
    template_phone = "\+7 \(\d{3}\) \d{3}(-\d{2}){2}"

    return len(phone) == 18 and match(template_phone, phone)
