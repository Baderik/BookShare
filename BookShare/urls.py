from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("authentication.urls")),
    path('articles/', include("articles.urls")),
    path('user/', include("people.urls")),
    path('', include("index.urls"))
]
