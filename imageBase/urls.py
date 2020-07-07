from django.urls import path

from imageBase.views import UploadView, GetView


urlpatterns = [
    path("", UploadView.as_view(), name="Upload"),
    path("<str:iid>/", GetView.as_view(), name="Get"),
]
