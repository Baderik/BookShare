from django.shortcuts import render, redirect
from django.views import View


class IndexView(View):
    @staticmethod
    def get(request):
        return redirect("search/")


class SearchView(View):
    @staticmethod
    def get(request):
        return render(request, "articles/search.html",
                      {
                          "user": request.user
                      })


class ArticleView(View):
    @staticmethod
    def get(request):
        return render(request, "articles/article.html",
                      {
                          "user": request.user
                      })


class AddView(View):
    @staticmethod
    def get(request):
        return render(request, "articles/editArticle.html",
                      {
                          "user": request.user
                      })


class EditView(View):
    @staticmethod
    def get(request):
        return render(request, "articles/editArticle.html",
                      {
                          "user": request.user
                      })
