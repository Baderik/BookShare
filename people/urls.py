from django.urls import path
from people.views import IndexView, ProfileView, SettingsView

urlpatterns = [
    path("", IndexView.as_view()),
    path("<int:uid>/", ProfileView.as_view()),
    path("settings/", SettingsView.as_view())
]
