from django.shortcuts import render, redirect
from django.views import View


class IndexView(View):
    @staticmethod
    def get(request):
        return redirect("1/")


class ProfileView(View):
    @staticmethod
    def get(request, uid):
        return render(request, "people/profile.html")


class SettingsView(View):
    @staticmethod
    def get(request):
        return render(request, "people/settings.html")
