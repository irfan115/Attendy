from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label=(u"email"))
    password = forms.CharField(
        label=(u"Password"), widget=forms.PasswordInput(render_value=False))