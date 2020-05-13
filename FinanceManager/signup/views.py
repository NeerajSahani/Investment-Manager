from django.contrib.auth.models import User

from . import forms
from . import models
from django.views import generic
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(never_cache, 'dispatch')
class SignupView(generic.FormView):
    form_class = forms.SignupForm
    template_name = 'signup/signup.html'
    success_url = ''


@method_decorator(never_cache, 'dispatch')
class Registration(generic.CreateView, SuccessMessageMixin):
    form_class = forms.SignupForm
    success_url = '/login'
    context_object_name = 'form'
    template_name = 'signup/signup.html'
    success_message = "Activation link is sent to your Email\nActivate Account before Login"

    def form_valid(self, form):
        form.instance.is_active = False
        mail_subject = 'Activate your account'
        message = render_to_string('signup/confirmation_email.html', {
            'user': form.instance,
            'domain': get_current_site(self.request).domain,
            'uid': urlsafe_base64_encode(force_bytes(form.instance.username)),
            'token': account_activation_token.make_token(form.instance),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        messages.success(self.request, "Activation link is sent to your Email\nActivate Account before Login")
        return super(Registration, self).form_valid(form)


@never_cache
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = models.CustomUser.objects.get(username=uid)
    except Exception:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('signup:loginView')
    else:
        return HttpResponse('Activation link is invalid!')


@never_cache
def login_view(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'successfully logged in')
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
            else:
                messages.error(request, 'You did not verify your email')
            return redirect('analyzer:indexView')

        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                messages.error(request, 'You did not verify your email')
            else:
                messages.error(request, "Password did not match. Try again")
            return redirect('signup:loginView')

        except User.DoesNotExist:
            messages.error(request, "User Not found please signup")
            return redirect('signup:signupView')

    else:
        return render(request, 'signup/login.html')


@never_cache
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged Out')
    return redirect('analyzer:indexView')


class ProfileView(generic.DetailView):
    model = models.CustomUser
    template_name = 'signup/ProfleView.html'
