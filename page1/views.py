from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def home(request):
	if request.user.groups.filter(name="parent"):
                print('parent group !')
                return render(request, 'parentcomponents/parentHomePage.html')
	return render(request, 'page1/homepage.html')


def Registration(request):
	return render(request, 'page1/register.html')
