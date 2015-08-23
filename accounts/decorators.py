"""
Created on Dec 3, 2014

@author: Faizan
"""
import functools
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from accounts.models import Teacher


def not_login_required(view_func):
    """
    Decorator where we need to insure that user is not logged in for example sign in page which should only be visible
    to users that are not logged in.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_anonymous():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('landing_page'))

    return wrapper

# parent required decorators


def parent_required(view_func):
    """
    Decorator for views that checks that the user is logged in and it is also parent type user.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.user_role == PayzatUser.PARENT and not user.payzat_parent.is_deleted:
                if user.payzat_parent.subscription == PayzatStudent.SUBSCRIBED:
                    students = PayzatStudent.objects.filter(
                        parent=user.payzat_parent,
                        subscription=PayzatStudent.SUBSCRIBED,
                        school__subscription__subscription_enddate__lt=timezone.now().date())
                    for student in students:
                        student.subscription = PayzatStudent.TRIAL_END
                        student.save()

                    if PayzatStudent.objects.filter(parent=user.payzat_parent, subscription=PayzatStudent.SUBSCRIBED).count() <= 0:
                        user.payzat_parent.subscription = PayzatStudent.TRIAL_END
                        user.payzat_parent.save()
                return view_func(request, *args, **kwargs)
            else:
                messages.add_message(
                    request, messages.ERROR, _("You are not authorized to perform this action."))
                return HttpResponseRedirect(reverse('landing_page'))
        else:
            messages.add_message(request, messages.ERROR, _(
                "You must be logged in before performing this operation."))
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrapper


def not_expired_parent_required(view_func):
    """
    Decorator for views that checks that the user is logged in and it is also parent type user.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.user_role == PayzatUser.PARENT:
                if user.payzat_parent.subscription == 0 and not user.payzat_parent.is_first:
                    return view_func(request, *args, **kwargs)
                elif user.payzat_parent.subscription == 2:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.add_message(
                        request, messages.ERROR, _("Your Trial period expired.Please buy subscription."))
                    return HttpResponseRedirect(reverse('landing_page'))
            else:
                messages.add_message(
                    request, messages.ERROR, _("You are not authorized to perform this action."))
                return HttpResponseRedirect(reverse('landing_page'))
        else:
            messages.add_message(request, messages.ERROR, _(
                "You must be logged in before performing this operation."))
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrapper


def student_required(view_func):
    """
    Decorator for views that checks that the user is logged in and it is also student type user.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.user_role == PayzatUser.STUDENT:
                return view_func(request, *args, **kwargs)
            else:
                messages.add_message(
                    request, messages.ERROR, _("You are not authorized to perform this action."))
                return HttpResponseRedirect(reverse('landing_page'))
        else:
            messages.add_message(request, messages.ERROR, _(
                "You must be logged in before performing this operation."))
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrapper


def school_required(view_func):
    """
    Decorator for views that checks that the user is logged in and it is also school type user.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.user_role == PayzatUser.SCHOOL:
                return view_func(request, *args, **kwargs)
            else:
                messages.add_message(
                    request, messages.ERROR, _("You are not authorized to perform this action."))
                return HttpResponseRedirect(reverse('landing_page'))
        else:
            messages.add_message(request, messages.ERROR, _(
                "You must be logged in before performing this operation."))
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrapper

# decorator for redirection to home


def redirect_to_home(view_func):
    """
    Decorator for which will redirect user to Parent home page if parent type user has logged in.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.user_role == PayzatUser.PARENT:
                return HttpResponseRedirect(verify_parent(request,
                                   reverse('parent:parent_home')))
            elif user.user_role == PayzatUser.STUDENT:
                return HttpResponseRedirect(verify_student(request,
                                   reverse('student:student_home')))
            elif user.user_role == PayzatUser.SCHOOL:
                return HttpResponseRedirect(verify_school(request.user.payzat_school.is_deleted,
                                   request, reverse('school:school_home')))
            elif user.user_role == PayzatUser.MERCHANT:
                return HttpResponseRedirect(verify_schools_list(request,
                                   reverse('merchant:merchant_home')))
            elif user.user_role == PayzatUser.ADMIN:
                return HttpResponseRedirect(reverse('admin:index'))
            else:
                messages.add_message(
                    request, messages.ERROR, _("You are not authorized to perform this action"))
                return HttpResponseRedirect(reverse('landing_page'))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def verify_parent(request, redirect):
    is_deleted = request.user.payzat_parent.is_deleted
    return verify_school(is_deleted, request, redirect)


def verify_student(request, redirect):
    student_deleted = request.user.payzat_student.is_deleted
    is_deleted = request.user.payzat_student.school.is_deleted
    if student_deleted:
        is_deleted = student_deleted
    return verify_school(is_deleted, request, redirect)


def verify_school(is_deleted, request, redirect):
    if is_deleted:
        messages.add_message(
            request, messages.ERROR, _("You are not authorized to perform this action"))
        [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == request.user.id]
        return '/'
    else:
        return redirect


def verify_schools_list(request, redirect):
    schools = request.user.payzat_merchant.schools.filter(is_deleted=False)
    if len(schools) == 0:
        return verify_school(True, request, redirect)
    return redirect

# decorator for redirection to disable device for parent, student, school
# to use appropriate permissions
def redirect_to_disable_device(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.user_role == PayzatUser.PARENT:
                return HttpResponseRedirect(reverse('parent:enable_disable_student_device', kwargs=kwargs))
            elif user.user_role == PayzatUser.STUDENT:
                return HttpResponseRedirect(reverse('student:enable_disable_student_device', kwargs=kwargs))
            elif user.user_role == PayzatUser.SCHOOL:
                return HttpResponseRedirect(reverse('school:enable_disable_student_device', kwargs=kwargs))
            else:
                messages.add_message(
                    request, messages.ERROR, _("You are not authorized to perform this action"))
                return HttpResponseRedirect(reverse('landing_page'))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper

# decorator for redirection to delete device for parent, student, school
# to use appropriate permissions


def redirect_to_delete_device(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.user_role == PayzatUser.PARENT:
                return HttpResponseRedirect(reverse('parent:delete_student_device', kwargs=kwargs))
            elif user.user_role == PayzatUser.SCHOOL:
                return HttpResponseRedirect(reverse('school:delete_student_device', kwargs=kwargs))
            else:
                messages.add_message(
                    request, messages.ERROR, _("You are not authorized to perform this action"))
                return HttpResponseRedirect(reverse('device:list_device'))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def merchant_required(view_func):
    """
    Decorator for views that checks that the user is logged in and it is also merchant type user.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.user_role == PayzatUser.MERCHANT:
                return view_func(request, *args, **kwargs)
            else:
                messages.add_message(
                    request, messages.ERROR, _("You are not authorized to perform this action."))
                return HttpResponseRedirect(reverse('landing_page'))
        else:
            messages.add_message(request, messages.ERROR, _(
                "You must be logged in before performing this operation."))
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrapper


def superadmin_required(view_func):
    """
    Decorator for views that checks that the user is logged in and it is also super admin type user.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.user_role == PayzatUser.ADMIN and user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                messages.add_message(
                    request, messages.ERROR, _("You are not authorized to perform this action."))
                return HttpResponseRedirect(reverse('landing_page'))
        else:
            messages.add_message(request, messages.ERROR, _(
                "You must be logged in before performing this operation."))
            return HttpResponseRedirect(reverse('xadmin:index'))

    return wrapper
