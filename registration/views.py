from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from registration import config
from registration.forms import RegistrationForm, LoginForm
from django.db import transaction
from ems.models import UserProfile

class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    @method_decorator(csrf_protect)
    @transaction.atomic
    def dispatch(self, *args, **kwargs):
        with transaction.atomic():
            return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        user_profile = User.objects.get(username=form.get_user)
        user_profile.userprofile.logins += 1
        user_profile.userprofile.save()
        user_profile.save()
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        try:
            return config.LOGIN_REDIRECT_URL
        except:
            return "/accounts/profile/"


class LogoutView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LogoutView, self).dispatch(*args, **kwargs)

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(config.LOGOUT_REDIRECT_URL)


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm

    @method_decorator(csrf_protect)
    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(config.INDEX_REDIRECT_URL)
        else:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)
            #with transaction.atomic():
            #    return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
        )
        user.is_active = True
        user.is_staff = True
        user.userprofile.mobile = form.cleaned_data['mobile']
        user.userprofile.qq = form.cleaned_data['qq']
        user.userprofile.user_type = u'MEMBER'
        user.userprofile.save()
        user.save()

        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse('register-success')


class RegisterSuccessView(TemplateView):
    template_name = 'registration/success.html'
