from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import *
from .tokens import account_activation_token

# Create your views here.
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

			message = render_to_string('account_activation_mail.html', {
				'user': user,
				'domain': site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})

			user.email_user(subject, message)

			return redirect('')
		else:
			return render(request, 'register.html', {'form': form})

	return redirect('register')

@login_required()
def post(request):

	return HttpResponse('This is the home page')
