from django import forms

from articles.models import Article, Tag


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('author', 'seen', 'date')
        widgets = {
            'tittle': forms.TextInput(attrs={
                "placeholder": "Новый заголовок",
                "class": "offset-2 col-9 offset-lg-0 col-lg-8"
            }),
            'description': forms.Textarea(attrs={"placeholder": "Новое описание",
                                                 "rows": "",
                                                 "cols": ""}),
            'avatar': forms.HiddenInput(attrs={"value": 0}),
            'phone': forms.CheckboxInput(attrs={
                "class": "toggle",
                "data-disabled-title": "Вы не указали номер телефона"
                }),
            'email': forms.CheckboxInput(attrs={"class": "toggle"}),
            'vk': forms.CheckboxInput(attrs={
                "class": "toggle",
                "data-disabled-title": "Вы не привязали аккаунт ВКонтакте"
                }),
            'facebook': forms.CheckboxInput(attrs={
                "class": "toggle",
                "data-disabled-title": "Вы не привязали аккаунт Facebook"
                }),
            'twitter': forms.CheckboxInput(attrs={
                "class": "toggle",
                "data-disabled-title": "Вы не привязали аккаунт Twitter"
                }),
            'odnoklassniki': forms.CheckboxInput(attrs={
                "class": "toggle",
                "data-disabled-title": "Вы не привязали аккаунт Одноклассники"
                }),
            'telegram': forms.CheckboxInput(attrs={
                "class": "toggle",
                "data-disabled-title": "Вы не указали номер телефона"
                }),
            'whatsapp': forms.CheckboxInput(attrs={
                "class": "toggle",
                "data-disabled-title": "Вы не указали номер телефона"
                }),
            'viber': forms.CheckboxInput(attrs={
                "class": "toggle",
                "data-disabled-title": "Вы не указали номер телефона"
                }),
        }


class SearchForm(forms.Form):
    search = forms.CharField(required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects,
                                          required=False)
    firstArticle = forms.IntegerField(widget=forms.HiddenInput())
    tags.widget.attrs["style"] = "display: none;"
    firstArticle.widget.attrs["value"] = 0
