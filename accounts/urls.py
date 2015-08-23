from django.conf.urls import patterns, url
from accounts.views import PasswordResetView, ConfirmEmailView, Dashboard

urlpatterns = patterns('',
                       #url(r'^login/$', LoginView.as_view(), name="accounts_login"),
                       url(r"^confirm_email/(?P<key>\w+)/$",
                           ConfirmEmailView.as_view(), name="accounts_confirm_email"),
                       url(r"^password/reset/$", PasswordResetView.as_view(),
                           name="accounts_password_reset"),
                       url(r"^dashboard/$", Dashboard.as_view(),
                           name="dashboard"),

                       )
