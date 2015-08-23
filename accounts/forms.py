
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from accounts.forms import SignupForm


class SignUpForm(SignupForm):
    MIN_LENGTH = settings.PASSWORD_MIN_LENGTH
    first_name = forms.CharField(
        max_length=30, label=_('First Name'))
    last_name = forms.CharField(
        max_length=30, label=_('Last Name'))
    mobile_phone = forms.CharField(
        max_length=30, label=_('Mobile Phone'))

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        del self.fields["username"]

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # At least MIN_LENGTH long
        if len(password) < self.MIN_LENGTH:
            raise forms.ValidationError(
                "The password must be at least %d characters long." % self.MIN_LENGTH)

        # At least one letter and one non-letter
        first_isalpha = password[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password):
            raise forms.ValidationError("The password must contain at least one letter and at least one digit or"
                                        " punctuation character.")
        return password
