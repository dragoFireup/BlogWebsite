from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import *
from .tokens import account_activation_token
from .models import Blog


def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "GET":
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False

            user.save()

            site = get_current_site(request)

            subject = 'Activate your Account'

            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject, message="", html_message=message)

            return redirect('home')
        else:
            return render(request, 'register.html', {'form': form})

    return redirect('register')


def login_request(request):
    """
    This function logins in a user if the credentials are valid
    :param request:
    :return: render template if get or login and redirect if post
    """

    if request.user.is_authenticated:
            return redirect('home')

    message = None
    if request.method == 'GET':
        form = LoginForm()

    elif request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user.profile.email_confirmed is False:
                message = 'Please activate your account'
            else:
                login(request, user)
                return redirect('home')
        else:
            message = 'Invalid username or password'

    return render(request, 'login.html', {'form': form, 'message': message})


def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


@login_required()
def home(request):
    return render(request, 'home.html')


def total(request):
    return JsonResponse({'count': list(Blog.objects.values_list('id', flat=True))})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and user.profile.email_confirmed is True:
        return redirect('home')

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return redirect('login')
