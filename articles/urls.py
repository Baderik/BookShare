from django.urls import path
from articles.views import IndexView, SearchView, ArticleView, AddView, EditView

urlpatterns = [
    path("", IndexView.as_view()),
    path("search/", SearchView.as_view()),
    path("<int:aid>/", ArticleView.as_view()),
    path("add/", AddView.as_view()),
    path("edit/", EditView.as_view()),
]
