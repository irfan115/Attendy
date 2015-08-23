from django import forms
from accounts.models import Teacher
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField


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
    
