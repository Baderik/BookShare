from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse

from random import choice

from articles.forms import ArticleForm
from articles.models import Article, Quote, Tag
from imageBase.forms import UploadImageForm


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

        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        form.save_m2m()

        return JsonResponse({"code": "303",
                             "message": "Вам туда",
                             "location": f"../{new_post.id}/"})


class SearchView(View):
    @staticmethod
    def get(request):
        return render(request, "articles/search.html",
                      {
                          "user": request.user,
                          "quote": choice(Quote.objects.all()),
                          "subjects": Tag.objects.filter(
                              group="subject").order_by("value"),
                          "classrooms": Tag.objects.filter(
                              group="classroom")
                      })


class ArticleView(View):
    @staticmethod
    def get(request, aid):
        article = get_object_or_404(Article, id=aid)

        return render(request, "articles/article.html",
                      {
                          "user": request.user,
                          "article": article,
                          "is_owner": request.user.id == article.author.id,
                          "subjects": article.tags.all().filter(
                              group="subject").order_by("value"),
                          "classrooms": article.tags.all().filter(
                              group="classroom")
                      })

    @staticmethod
    def post(request, aid):
        article = get_object_or_404(Article, id=aid)

        if not request.user.is_authenticated or\
                not request.user.is_active or \
                request.user.id != article.author.id:
            return JsonResponse({"code": "403", "message": "Вам туда нельзя"})

        form = ArticleForm(request.POST, instance=article)

        if not form.is_valid() or \
                not processing_checkbox(form, request.user):
            return JsonResponse(
                {"code": "400",
                 "message": "Проверьте правильно ли заполнены поля"})

        new_post = form.save(commit=False)
        new_post.save()
        form.save_m2m()

        return JsonResponse({"code": "303",
                             "message": "Вам туда",
                             "location": f"../../{new_post.id}/"})


class AddView(View):
    @staticmethod
    def get(request):
        return render(request, "articles/editArticle.html",
                      {
                          "user": request.user,
                          "form": ArticleForm(),
                          "imageForm": UploadImageForm(),
                          "subjects": Tag.objects.filter(
                              group="subject").order_by("value"),
                          "classrooms": Tag.objects.filter(
                              group="classroom")
                      })


class EditView(View):
    @staticmethod
    def get(request, aid):
        article = get_object_or_404(Article, id=aid)

        if not request.user.is_authenticated or\
                not request.user.is_active \
                or request.user.pk != article.author.pk:
            return redirect('/')

        return render(request, "articles/editArticle.html",
                      {
                          "user": request.user,
                          "form": ArticleForm(instance=article),
                          "id": article.id,
                          "imageForm": UploadImageForm(),
                          "subjects": Tag.objects.filter(
                              group="subject").order_by("value"),
                          "classrooms": Tag.objects.filter(
                              group="classroom"),
                          "subjectsArticle": article.tags.all().filter(
                              group="subject").order_by("value"),
                          "classroomsArticle": article.tags.all().filter(
                              group="classroom")
                      })


def processing_messengers(form):
    messengers = ("telegram", "whatsapp", "viber")
    if not form.cleaned_data["phone"]:
        for messenger in messengers:
            if form.cleaned_data[messenger]:
                return False

    return True


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
    print("social")
    if not processing_social(form, user):
        return False
    print("messengers")
    if not processing_messengers(form):
        return False

    print("data")

    return (form.cleaned_data["phone"] or
            form.cleaned_data["email"] or
            form.cleaned_data["vk"] or
            form.cleaned_data["facebook"] or
            form.cleaned_data["twitter"] or
            form.cleaned_data["odnoklassniki"])
