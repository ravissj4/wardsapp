from django.db.models.signals import form_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(form_save, sender=User)
def create_student(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		
@receiver(form_save, sender=User)
def save_student(sender, instance, **kwargs):
	instance.profile.save()