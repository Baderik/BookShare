from django import forms

from people.models import Profile


class SettingsForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Классный пароль"}))
    password_again = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Ещё раз"}))

    email.widget.attrs["placeholder"] = "Моя почта"

    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'surname': forms.TextInput(attrs={"placeholder": "Моя фамилия"}),
            'name': forms.TextInput(attrs={"placeholder": "Моё имя"}),
            'middle_name': forms.TextInput(attrs={"placeholder": "Моё отчество"}),
            'phone': forms.TextInput(attrs={"placeholder": "Мой телефон"}),
            'image': forms.HiddenInput(),
            'about': forms.Textarea(attrs={"placeholder": "Пару слов",
                                           "rows": "5"})
        }

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = False
