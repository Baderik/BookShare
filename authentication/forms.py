from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField()
    email.widget.attrs["class"] = "AuthField"
    email.widget.attrs["placeholder"] = "Почта"


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    email.widget.attrs["placeholder"] = "Почта"
    password.widget.attrs["placeholder"] = "Пароль"
