from django import forms

from articles.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('author', 'status', 'date')
        widgets = {
            'tittle': forms.TextInput(attrs={
                "placeholder": "Новый заголовок",
                "class": "offset-2 col-9 offset-lg-0 col-lg-8"
            }),
            'description': forms.Textarea(attrs={"placeholder": "Новое описание",
                                                 "rows": "",
                                                 "cols": ""}),
            'images': forms.HiddenInput(),
            'tags': forms.HiddenInput(),
            'avatar': forms.HiddenInput()
        }
