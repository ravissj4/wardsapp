from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Login(models.Model):
	username = models.ForeignKey(User, on_delete=models.CASCADE)
	password = models.CharField(max_length=100)

def __str__ (self):
	return self.username