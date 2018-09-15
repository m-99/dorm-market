# Create your models here.

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

class Order(models.Model):
    trader_name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item_name = models.TextField(max_length=500, blank=True)
    item_price = models.TextField(max_length=500, blank=True)
    image_url = models.TextField(max_length=500, blank=True)
    item_type = models.CharField(max_length=1, blank=True)
    price = models.IntegerField(default=0)
    time_posted = models.DateTimeField(auto_now_add=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()