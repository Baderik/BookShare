from django.shortcuts import HttpResponse, redirect, get_object_or_404, render
from django.views import View
from django.http import JsonResponse

from imageBase.models import ImageModel
from imageBase.forms import UploadImageForm

from PIL import Image

import os


class UploadView(View):
    @staticmethod
    def get(request):
        return render(request, "imageBase/index.html", {"form": UploadImageForm()})

    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return redirect("/")

        form = UploadImageForm(request.POST, request.FILES)

        if not form.is_valid():
            return HttpResponse(status=400)

        image = form.save()

        return JsonResponse({"id": image.id})


class GetView(View):
    @staticmethod
    def get(request, iid):
        image = get_object_or_404(ImageModel, pk=iid)

        return redirect(image.image.url)
