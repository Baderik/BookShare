from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse

from people.forms import SettingsForm


class IndexView(View):
    @staticmethod
    def get(request):
        return redirect("1/")


class ProfileView(View):
    @staticmethod
    def get(request, uid):
        return render(request, "people/profile.html")

    @staticmethod
    def post(request, uid, *args, **kwargs):
        if not request.user.is_authenticated or uid != request.user.pk:
            return JsonResponse({"code": "403", "message": "Вам туда нельзя"})

        form = SettingsForm(request.POST, instance=request.user.profile)

        if not form.is_valid():
            return JsonResponse({"code": "400", "message": "Проверьте правильно ли вы заполнили поля"})

        message = []

        if request.user.email != form.cleaned_data["email"]:
            request.user.email = form.cleaned_data["email"]
            request.user.is_active_email = False
            # Отправить письмо с подтверждением почты
            message.append("Ваша почта изменён")

        if form.cleaned_data["password"]:
            if form.cleaned_data["password"] == form.cleaned_data["password_again"]:
                message.append("Ваш пароль изменён")

            else:
                return JsonResponse({"code": "400", "message": "Пароли не совпадают"})

        request.user.is_active = True
        request.user.save()

        if not message:
            message = ["Сохранено"]

        return JsonResponse({"code": "200", "message": "\n".join(message)})


class SettingsView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return render(request, "people/settings.html",
                          {"form": SettingsForm()})

        return redirect("/")
