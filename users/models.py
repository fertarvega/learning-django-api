""" Profile - BaseUser Model"""
from django.db import models
from django.contrib.auth.models import User


class Profile (models.Model):
    """ Adding data to Base User model """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(blank=True, null=True)
    header_img = models.ImageField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    followers = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    posts = models.IntegerField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.user.get_full_name()