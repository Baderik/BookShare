from django.contrib import admin

from articles.models import Article, Quote, Tag

admin.site.register(Article)
admin.site.register(Quote)
admin.site.register(Tag)
