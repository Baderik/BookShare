from django.contrib import admin

from articles.models import Article, Quote

admin.site.register(Article)
admin.site.register(Quote)
