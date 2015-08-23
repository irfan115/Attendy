from django import forms
from django.db import transaction
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Teacher


class UserCreationForm(forms.ModelForm):

    """
        This Custom Admin Form to save Parent user.
    """

    MIN_LENGTH = settings.PASSWORD_MIN_LENGTH
    password1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput(render_value=True))
    password2 = forms.CharField(
        label=_('Password confirmation'), widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = Teacher
        fields = (
    		'first_name', 'last_name', 'email', 'is_staff','is_active', 'user_role')

    def __init__(self, *args, **kwargs):

        super(UserCreationForm, self).__init__(*args, **kwargs)

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

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

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(
            commit=False)

        with transaction.atomic():
            try:
                user.set_password(self.cleaned_data["password1"])
                user.save()

            except Exception as e:
                logger.error("Exception occurred while creating Teacher",e)

        return user


class UserChangeForm(forms.ModelForm):

    """
        This Custom Admin Form to update Parent user.
    """

    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"%s\">this form</a>." % ('password')))
    class Meta:
        model = Teacher
    	fields = (
    		'first_name', 'last_name', 'email', 'is_staff','is_active', 'user_role')

  

