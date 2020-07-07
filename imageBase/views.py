from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.http import JsonResponse

from imageBase.models import ImageModel
from imageBase.forms import UploadImageForm


class UploadView(View):
    @staticmethod
    def get(request):
        return render(request, "imageBase/index.html",
                      {"form": UploadImageForm()})

    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return JsonResponse({"code": "403",
                                 "message": "Вам не сюда"})

        form = UploadImageForm(request.POST, request.FILES)

        if not form.is_valid():
            return JsonResponse({
                "code": "400",
                "message": "Проверьте правильно ли вы заполнили поля"})

        image = form.save()

        return JsonResponse({"code": "200",
                             "message": "Congratualtions",
                             "id": image.id})


class GetView(View):
    @staticmethod
    def get(request, iid):
        image = get_object_or_404(ImageModel, pk=iid)

        return redirect(image.image.url)
