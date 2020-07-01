from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse

from articles.forms import ArticleForm
from articles.models import Article


class IndexView(View):
    @staticmethod
    def get(request):
        return redirect("search/")

    @staticmethod
    def post(request):
        if not request.user.is_authenticated or not request.user.is_active:
            return JsonResponse({"code": "403", "message": "Вам туда нельзя"})

        form = ArticleForm(request.POST)

        if not form.is_valid() or not processing_checkbox(form, request.user):
            return JsonResponse(
                {"code": "400",
                 "message": "Проверьте правильно ли заполнены поля"})

        print(form.cleaned_data["phone"])

        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()

        return JsonResponse({"code": "303",
                             "message": "Вам туда",
                             "location": f"../{new_post.id}/"})


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
                          "user": request.user,
                          "form": ArticleForm()
                      })


class EditView(View):
    @staticmethod
    def get(request, aid):
        return render(request, "articles/editArticle.html",
                      {
                          "user": request.user
                      })


def processing_messengers(form):
    messengers = ("telegram", "whatsapp", "viber")
    if not form.cleaned_data["phone"]:
        for messenger in messengers:
            if form.cleaned_data[messenger]:
                return False


def processing_social(form, user):
    if form.cleaned_data["phone"] and not user.profile.phone:
        return False
    # Вместо False должна быть проверка социальной сети у пользователя
    if form.cleaned_data["vk"] and not False:
        return False

    if form.cleaned_data["facebook"] and not False:
        return False

    if form.cleaned_data["twitter"] and not False:
        return False

    if form.cleaned_data["odnoklassniki"] and not False:
        return False

    return True


def processing_checkbox(form, user):
    if not processing_social(form, user):
        return False
    if not processing_messengers(form):
        return False

    return (form.cleaned_data["phone"] or
            form.cleaned_data["email"] or
            form.cleaned_data["vk"] or
            form.cleaned_data["facebook"] or
            form.cleaned_data["twitter"] or
            form.cleaned_data["odnoklassniki"])
