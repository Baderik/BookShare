from django.shortcuts import redirect
from django.views import View


class IndexView(View):
    @staticmethod
    def get(request):
        return redirect("/articles/")
