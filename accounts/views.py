import string
import random

from django.shortcuts import render
from django.template.context import RequestContext
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.utils.http import int_to_base36
from django.core.urlresolvers import reverse
from accounts.hooks import hookset

from accounts.views import SignupView, LoginView, ConfirmEmailView, PasswordResetView
from accounts.forms import LoginEmailForm
from accounts.models import EmailAddress
from django.views.generic.base import TemplateView
from accounts.forms import SignUpForm

from accounts.models import Teacher
from accounts.decorators import redirect_to_home


class LoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginEmailForm

    @method_decorator(redirect_to_home)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name, {}, context_instance=RequestContext(request))


class ParentSignUpView(SignupView):
    form_class = SignUpForm

    def create_user(self, form, commit=True, **kwargs):
        user = super(ParentSignUpView, self).create_user(
            form=form, commit=False,  **kwargs)
        user.first_name = form.cleaned_data.get(
            "first_name")
        user.last_name = form.cleaned_data.get("last_name")
        user.is_active = False

        user.user_role = PayzatUser.PARENT
        if commit:
            user.save()

        return user

    def after_signup(self, form):
        mobile_phone = form.cleaned_data.get(
            "mobile_phone", None)
        payzat_parent = PayzatParent(
            mobile_phone=mobile_phone, user=self.created_user)
        payzat_parent.save()

        messages.success(self.request, 'Thanks for registering in Attendy. Confirmation email is been sent to your '
                                       'accounts. Kindly check your inbox.')
        super(ParentSignUpView, self).after_signup(form)

    def generate_username(self, form):
        # django-user-accountss requires us to generate dummy username
        # unfortunately.
        username = form.cleaned_data.get('email', ''.join(random.SystemRandom().choice(string.uppercase +
                                                                                       string.digits) for _ in xrange(15)))
        return username


class ConfirmEmailView(ConfirmEmailView):

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm()
        self.after_confirmation(confirmation)
        redirect_url = self.get_redirect_url()
        if not redirect_url:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        if self.messages.get("email_confirmed"):
            messages.add_message(
                self.request,
                self.messages["email_confirmed"]["level"],
                self.messages["email_confirmed"]["text"].format(**{
                    "email": confirmation.email_address.email
                })
            )
        return redirect(redirect_url)


class PasswordResetView(PasswordResetView):

    def send_email(self, email):
        User = get_user_model()
        protocol = getattr(
            settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = get_current_site(self.request)
        email_qs = EmailAddress.objects.filter(
            email__iexact=email)
        for user in User.objects.filter(pk__in=email_qs.values("user")):
            uid = int_to_base36(user.id)
            token = self.make_token(user)
            password_reset_url = "{0}://{1}{2}".format(
                protocol,
                current_site.domain,
                reverse("django-user-accounts:accounts_password_reset_token",
                        kwargs=dict(uidb36=uid, token=token))
            )
            ctx = {
                "user": user,
                "current_site": current_site,
                "password_reset_url": password_reset_url,
            }
            hookset.send_password_reset_email(
                [user.email], ctx)


class Dashboard(TemplateView):

    @method_decorator(redirect_to_home)
    def dispatch(self, request, *args, **kwargs):
        return super(Dashboard, self).dispatch(request, *args, **kwargs)