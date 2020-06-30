from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import get_user_model
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
            "is_owner": request.user.id == user.id
        })

    @staticmethod
    def post(request, uid, *args, **kwargs):
        if not request.user.is_authenticated or uid != request.user.pk:
            return JsonResponse({"code": "403", "message": "Вам туда нельзя"})

        form = SettingsForm(request.POST, instance=request.user.profile)

        if not form.is_valid():
            return JsonResponse({"code": "400",
                                 "message": "Проверьте правильно ли вы заполнили поля"})

        message = []

        if request.user.email != form.cleaned_data["email"]:
            if get_user_model().objects.filter(email=form.cleaned_data["email"]):
                return JsonResponse({"code": "400",
                                     "message": "Эту почту уже кто-то использует"})

            request.user.email = form.cleaned_data["email"]
            request.user.is_active_email = False
            # Отправить письмо с подтверждением почты
            message.append("Ваша почта изменён")

        if form.cleaned_data["password"]:
            if form.cleaned_data["password"] == form.cleaned_data["password_again"]:
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
                              initial={
                                  "surname": request.user.profile.surname,
                                  "name": request.user.profile.name,
                                  "middle_name": request.user.profile.middle_name,
                                  "about": request.user.profile.about,
                                  "email": request.user.email,
                                  "phone": request.user.profile.phone,
                                  "image": request.user.profile.image
                              }
                          ),
                              "email": request.user.is_active_email,
                              "user": request.user
                          })

        return redirect("/")
