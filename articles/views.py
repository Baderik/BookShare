from django.shortcuts import render, redirect
from django.views import View


class IndexView(View):
    @staticmethod
    def get(request):
        return redirect("search/")


class SearchView(View):
    @staticmethod
    def get(request):
        return render(request, "articles/search.html")


class ArticleView(View):
    @staticmethod
    def get(request):
        return render(request, "articles/article.html")


class AddView(View):
    @staticmethod
    def get(request):
        return render(request, "articles/editArticle.html")


class EditView(View):
    @staticmethod
    def get(request):
        return render(request, "articles/editArticle.html")
