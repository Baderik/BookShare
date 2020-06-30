from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from articles.models import Article


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
    def get(request, aid):
        print(aid)
        article = get_object_or_404(Article, id=aid)

        return render(request, "articles/article.html",
                      {
                          "user": request.user,
                          "article": article,
                          "is_owner": request.user.id == article.author.id
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
