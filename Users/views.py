from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Your account has been created! You are now being redirected to login page to log in!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'Users/register.html', {'form': form})
'''
@login_required


def profile(request):
	return render(request, 'Users/profile.html')
'''