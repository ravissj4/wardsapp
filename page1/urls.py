from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='project-home'),
	path('register/', views.Registration, name='project-Registration'),
]